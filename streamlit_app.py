# streamlit_app.py
# Minimal image search UI for Squarespace embedding via <iframe>
# - Reads your JSON from GitHub
# - Searches description and clip_tags (case-insensitive)
# - Supports ?q=<term> in the URL so your Squarespace button/input can pass a query
# - Displays thumbnails that link to the original image URL

import re
import requests
import streamlit as st
import json

# Your canonical JSON raw links:
JSON_URL = "https://raw.githubusercontent.com/WhaleCancer/LichenThumbnail/main/images_for_squarespace_githubthumbs.json"
TERRITORIAL_URL = "https://raw.githubusercontent.com/WhaleCancer/LichenThumbnail/main/territorial_mapping.json"

st.set_page_config(page_title="Lichen Search", layout="wide")

# Force light mode
st.markdown("""
<style>
    .stApp {
        color-scheme: light;
    }
    .stApp > header {
        background-color: transparent;
    }
    .stApp > div > div > div > div {
        background-color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# --- Helpers -----------------------------------------------------------------
def get_initial_query() -> str:
    # Compatible with a wide range of Streamlit versions
    try:
        params = st.experimental_get_query_params()
        return (params.get("q", [""]) or [""])[0]
    except Exception:
        return ""

def set_query(q: str):
    try:
        st.experimental_set_query_params(q=q)
    except Exception:
        pass

@st.cache_data(ttl=300, show_spinner=False)
def load_data():
    # Cache for 5 minutes
    r = requests.get(JSON_URL, timeout=15)
    r.raise_for_status()
    data = r.json()
    if not isinstance(data, list):
        raise ValueError("JSON root is not a list")
    return data

@st.cache_data(ttl=300, show_spinner=False)
def load_territorial_data():
    # Cache for 5 minutes
    try:
        r = requests.get(TERRITORIAL_URL, timeout=15)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.warning(f"Could not load territorial data: {e}. Continuing without territorial information.")
        return {}

def norm(s):
    return (s or "").strip()

def highlight(text: str, term: str) -> str:
    if not term or not text:
        return norm(text)
    try:
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        return pattern.sub(lambda m: f"<mark>{m.group(0)}</mark>", text)
    except re.error:
        return text

def record_name(rec: dict) -> str:
    return rec.get("photo_name") or rec.get("Photo Name") or "Untitled"

def record_desc(rec: dict) -> str:
    return rec.get("description") or ""

def record_tags(rec: dict) -> str:
    return rec.get("clip_tags") or ""

def get_territorial_info(rec, territorial_data):
    """Get territorial information for a record"""
    photo_name = record_name(rec)
    return territorial_data.get(photo_name, {})

def get_all_territories(territorial_data):
    """Get list of all unique territories"""
    territories = set()
    for mapping in territorial_data.values():
        if mapping.get('first_nation'):
            territories.add(mapping['first_nation'])
    return sorted(list(territories))

def get_all_tags(data):
    """Extract all unique tags from the dataset"""
    all_tags = set()
    for rec in data:
        tags_str = record_tags(rec)
        if tags_str:
            # Split tags by common separators and clean them
            tags = [tag.strip() for tag in re.split(r'[,;|\n]', tags_str) if tag.strip()]
            all_tags.update(tags)
    return sorted(list(all_tags))

def get_selected_tags_from_session():
    """Get selected tags from session state"""
    return st.session_state.get('selected_tags', [])

def set_selected_tags_in_session(tags):
    """Set selected tags in session state"""
    st.session_state['selected_tags'] = tags

def search_records(data, term: str, territorial_data: dict, selected_territory: str = None, selected_tags: list = None):
    t = term.lower() if term else ""
    hits = []
    
    for r in data:
        # Check text search in description and tags (only if there's a search term)
        text_match = False
        if t:
            text_match = t in record_desc(r).lower() or t in record_tags(r).lower()
        
        # Check territorial search in text (only if there's a search term)
        territory_match = False
        if t and territorial_data:
            photo_name = record_name(r)
            territory_info = territorial_data.get(photo_name, {})
            first_nation = territory_info.get('first_nation', '').lower()
            territory_match = t in first_nation
        
        # Check territory filter
        territory_filter_match = True
        if selected_territory and selected_territory != "All Territories":
            photo_name = record_name(r)
            territory_info = territorial_data.get(photo_name, {})
            actual_territory = territory_info.get('first_nation', '')
            territory_filter_match = actual_territory == selected_territory
        
        # Check tag filter
        tag_filter_match = True
        if selected_tags:
            record_tags_str = record_tags(r).lower()
            # Check if any selected tag appears in the record's tags
            tag_filter_match = any(tag.lower() in record_tags_str for tag in selected_tags)
        
        # Include record based on search criteria:
        # - If there's a search term: match text/territory search AND territory filter AND tag filter
        # - If no search term but territory/tags selected: match territory filter AND tag filter
        if t:
            # Text search mode: match text/territory search AND territory filter AND tag filter
            if (text_match or territory_match) and territory_filter_match and tag_filter_match:
                hits.append(r)
        else:
            # Filter-only mode: match territory filter AND tag filter
            if territory_filter_match and tag_filter_match:
                hits.append(r)
    return hits

# --- UI ----------------------------------------------------------------------
st.title("Lichen Search")

# Introduction text
st.markdown("""
**Welcome to the Beta version of our Lichen re-launch!** 

We've moved away from offering Lichen photographs through a Shopify interface and instead are offering them directly through a search interface. You can use the search tools below to find images, but you will need to be granted access to the Lichen Google Drive to be able to access the full sized images.

While we are in this beta, we will be making changes to this page, the search interface, and the arrangement of searchable information. If you'd like to request access or provide feedback, please email **Sebastian** at [sebastian@organizingforchange.org](mailto:sebastian@organizingforchange.org).
""")

st.markdown("---")  # Add a separator line

# Read initial ?q= from URL (useful for embedding where you pass q from Squarespace)
initial_q = get_initial_query()

# Load data
with st.spinner("Loading image data…"):
    try:
        data = load_data()
        territorial_data = load_territorial_data()
        st.success(f"Successfully loaded {len(data)} images")
        if territorial_data:
            st.success(f"Loaded territorial data for {len(territorial_data)} images")
    except Exception as e:
        st.error(f"Could not fetch image data: {e}")
        st.stop()

# Input
with st.container():
    col1, col2 = st.columns([3, 1])
    
    with col1:
        term = st.text_input(
            "🔍 Search Images", 
            value=initial_q, 
            placeholder="e.g., lichen, bark, coastal, Secwepemc (or just select a territory to the right)",
            help="Search through image descriptions, tags, or territory names"
        ).strip()
        # Keep URL in sync so page refreshes/bookmarks preserve the query
        if term != initial_q:
            set_query(term)
    
    with col2:
        # Territory filter dropdown
        all_territories = ["All Territories"] + get_all_territories(territorial_data)
        selected_territory = st.selectbox(
            "🗺️ Territory Filter",
            all_territories,
            index=0,
            help="Select a territory to see all images from that First Nations territory, or combine with text search"
        )

# Tag Filter Section
# Get all unique tags first
all_tags = get_all_tags(data)

# Initialize session state for selected tags
if 'selected_tags' not in st.session_state:
    st.session_state['selected_tags'] = []

# Always expand the tag filter section to avoid closing issues
with st.expander("🏷️ Filter by Tags", expanded=True):
    if all_tags:
        
        # Select all / Select none buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Select All Tags", use_container_width=True):
                st.session_state['selected_tags'] = all_tags.copy()
        
        with col2:
            if st.button("Select None", use_container_width=True):
                st.session_state['selected_tags'] = []
        
        # Display tag checkboxes in columns
        st.write(f"**Available Tags ({len(all_tags)} total):**")
        
        # Create columns for tags (4 columns)
        cols = st.columns(4)
        selected_tags = []
        
        for i, tag in enumerate(all_tags):
            col_idx = i % 4
            with cols[col_idx]:
                is_selected = tag in st.session_state['selected_tags']
                if st.checkbox(tag, value=is_selected, key=f"tag_{tag}"):
                    selected_tags.append(tag)
        
        # Update session state
        st.session_state['selected_tags'] = selected_tags
        
        if selected_tags:
            st.info(f"📋 **{len(selected_tags)} tags selected:** {', '.join(selected_tags[:5])}{'...' if len(selected_tags) > 5 else ''}")
    else:
        st.info("No tags found in the dataset.")

# Calculate filtered results for status card
hits = search_records(data, term, territorial_data, selected_territory, selected_tags)
should_show_results = (
    term or 
    selected_territory != "All Territories" or 
    selected_tags
)

# Display dynamic filtering status message
if should_show_results:
    # Build descriptive message about current filters
    filter_description = []
    if term:
        filter_description.append(f"search term '{term}'")
    if selected_territory != "All Territories":
        filter_description.append(f"territory '{selected_territory}'")
    if selected_tags:
        filter_description.append(f"{len(selected_tags)} selected tag{'s' if len(selected_tags) != 1 else ''}")
    
    filter_text = ", ".join(filter_description)
    st.info(f"🎯 **{len(hits)} images** found matching your filters: {filter_text}")
else:
    st.info("🎯 **No filters applied** - Select a search term, territory, or tags to see filtered results")

# Content
# Use the selected_tags and hits we already calculated above

if not should_show_results:
    st.caption("Type a search term, select a territory, or choose tags to see images. You can also pass ?q=term in the URL when embedding.")
else:
    
    # Update the results message to be more informative
    filter_parts = []
    if term:
        filter_parts.append(f"'{term}'")
    if selected_territory != "All Territories":
        filter_parts.append(f"{selected_territory} territory")
    if selected_tags:
        filter_parts.append(f"{len(selected_tags)} tag(s)")
    
    if filter_parts:
        filter_text = " + ".join(filter_parts)
        st.write(f"Results for {filter_text}: {len(hits)}")
    else:
        st.write(f"Results: {len(hits)}")

    if not hits:
        if filter_parts:
            st.info(f"No images found matching: {filter_text}")
        else:
            st.info("No results.")
    else:
        # Display in a responsive grid
        cols_per_row = 3
        cols = st.columns(cols_per_row)

        for i, rec in enumerate(hits):
            c = cols[i % cols_per_row]
            with c:
                name = record_name(rec)
                thumb = rec.get("thumb_url")
                link = rec.get("image_url")
                desc = record_desc(rec)
                tags = record_tags(rec)
                
                # Get territorial information
                territory_info = get_territorial_info(rec, territorial_data)

                if thumb:
                    st.image(thumb)
                st.markdown(f"**{name}**")
                
                # Display territorial information
                if territory_info and territory_info.get('first_nation'):
                    st.markdown(f"🗺️ **{territory_info['first_nation']} Territory**")

                # Link to original image
                if link:
                    # link_button is convenient, but markdown works universally
                    st.markdown(f"[Open original]({link})")

                # Highlight matches in description and tags
                if desc:
                    st.markdown(highlight(desc, term), unsafe_allow_html=True)
                if tags:
                    st.caption(highlight(f"Tags: {tags}", term), unsafe_allow_html=True)

# Footer (optional)
st.markdown(
    """
    <div style="opacity:0.6; font-size:0.9em; margin-top:1rem;">
    Data source: GitHub JSON • Cached for 5 minutes
    </div>
    """,
    unsafe_allow_html=True,
)