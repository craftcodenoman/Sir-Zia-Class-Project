import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import requests
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="📚 Library Manager Pro",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
    
    :root {
        --primary-color: #7C3AED;
        --secondary-color: #10B981;
        --accent-color: #F59E0B;
        --background-color: #F8F9FA;
        --text-color: #1F2937;
        --card-color: #FFFFFF;
    }
    
    .stApp {
       
        background-position: center;
        background-attachment: fixed;
        font-family: 'Poppins', sans-serif;
        color: var(--text-color);
    }
    
    .main-header {
        background: linear-gradient(120deg, #7C3AED 0%, #10B981 100%);
        padding: 2.5rem;
        border-radius: 25px;
        color: white;
        text-align: center;
        margin-bottom: 2.5rem;
        box-shadow: 0 15px 30px rgba(124, 58, 237, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        transform: translateX(-100%);
        transition: 0.5s;
    }
    
    .main-header:hover::before {
        transform: translateX(100%);
    }
    
    .card {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        margin-bottom: 1.5rem;
        transition: all 0.4s ease;
        border: 1px solid rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(10px);
    }
    
    .card:hover {
        transform: translateY(-5px) scale(1.01);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.12);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #7C3AED, #10B981);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        color: white;
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        transform: translateX(-100%);
        transition: 0.5s;
    }
    
    .metric-card:hover::before {
        transform: translateX(100%);
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: 700;
        margin: 0.8rem 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .metric-label {
        font-size: 1.2rem;
        font-weight: 500;
        opacity: 0.95;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    .book-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
        gap: 2rem;
        padding: 1.5rem 0;
    }
    
    .book-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        transition: all 0.4s ease;
        border: 1px solid rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(10px);
    }
    
    .book-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.12);
    }
    
    .book-cover {
        width: 100%;
        height: 550px;
        object-fit: cover;
        transition: all 0.4s ease;
    }
    
    .book-card:hover .book-cover {
        transform: scale(1.05);
    }
    
    .book-info {
        padding: 1.8rem;
    }
    
    .book-title {
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 0.8rem;
        color: var(--text-color);
        line-height: 1.3;
    }
    
    .book-author {
        color: var(--text-color);
        opacity: 0.8;
        margin-bottom: 1.2rem;
        font-size: 1.1rem;
        font-weight: 500;
    }
    
    .book-status {
        display: inline-block;
        padding: 0.5rem 1.2rem;
        border-radius: 25px;
        font-size: 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .status-read {
        background: linear-gradient(45deg, #10B981, #059669);
        color: white;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.2);
    }
    
    .status-unread {
        background: linear-gradient(45deg, #F59E0B, #D97706);
        color: white;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.2);
    }
    
    .search-box {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2.5rem;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(10px);
    }
    
    .stTextInput>div>div>input {
        border-radius: 15px !important;
        padding: 1rem 1.2rem !important;
        border: 2px solid #E5E7EB !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #7C3AED !important;
        box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1) !important;
    }
    
    .stButton>button {
        border-radius: 15px !important;
        padding: 0.8rem 2.5rem !important;
        background: linear-gradient(120deg, #7C3AED 0%, #10B981 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        border: none !important;
        transition: all 0.4s ease !important;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.2) !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(124, 58, 237, 0.3) !important;
    }
    
    .stSelectbox>div>div {
        border-radius: 15px !important;
        border: 2px solid #E5E7EB !important;
    }
    
    .stSelectbox>div>div:focus-within {
        border-color: #7C3AED !important;
        box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1) !important;
    }
    
    .stCheckbox>div>div>div {
        border-radius: 15px !important;
    }
    
    .stCheckbox>div>div>div:checked {
        background-color: #7C3AED !important;
        border-color: #7C3AED !important;
    }
    
    .stProgress .st-bo {
        background-color: #7C3AED !important;
    }
    
    .stProgress .st-bp {
        background-color: #E5E7EB !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 15px;
        padding: 0.8rem 1.5rem;
        background: rgba(255, 255, 255, 0.95);
        border: 1px solid rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #7C3AED;
        color: white;
        border-color: #7C3AED;
    }
    
    .stTabs [aria-selected="true"] {
        background: #7C3AED !important;
        color: white !important;
        border-color: #7C3AED !important;
    }
    
    .stExpander {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
    }
    
    .stExpander:hover {
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.12);
    }
    
    .stExpander .streamlit-expanderHeader {
        border-radius: 20px;
        padding: 1.5rem;
        background: linear-gradient(120deg, #7C3AED 0%, #10B981 100%);
        color: white;
        font-weight: 600;
    }
    
    .stExpander .streamlit-expanderContent {
        padding: 1.5rem;
    }
    
    .stAlert {
        border-radius: 15px;
        border: none;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    }
    
    .stAlert[data-baseweb="notification"] {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .stAlert[data-baseweb="notification"].stAlert-success {
        border-left: 4px solid #10B981;
    }
    
    .stAlert[data-baseweb="notification"].stAlert-error {
        border-left: 4px solid #EF4444;
    }
    
    .stAlert[data-baseweb="notification"].stAlert-info {
        border-left: 4px solid #3B82F6;
    }
    
    .stAlert[data-baseweb="notification"].stAlert-warning {
        border-left: 4px solid #F59E0B;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'books' not in st.session_state:
    st.session_state.books = []
if 'current_id' not in st.session_state:
    st.session_state.current_id = 1
if 'reading_goal' not in st.session_state:
    st.session_state.reading_goal = 0
if 'favorites' not in st.session_state:
    st.session_state.favorites = set()

# Load and save functions
def save_books():
    with open('library.json', 'w') as f:
        json.dump(st.session_state.books, f)

def load_books():
    try:
        if os.path.exists('library.json'):
            with open('library.json', 'r') as f:
                st.session_state.books = json.load(f)
                if st.session_state.books:
                    st.session_state.current_id = max(book['id'] for book in st.session_state.books) + 1
    except Exception as e:
        st.error(f"Error loading library: {e}")

# Load books at startup
load_books()

# Sidebar navigation
st.sidebar.markdown("""
    <div style='text-align: center; padding: 1.5rem;'>
        <h1 style='color: #7C3AED; font-size: 1.8rem; font-weight: 700;'>📚 Library Manager Pro</h1>
        <p style='color: #6B7280; font-size: 0.9rem;'>Your Personal Reading Companion</p>
    </div>
""", unsafe_allow_html=True)

page = st.sidebar.radio("Navigation", ["Dashboard", "Add Books", "Manage Books", "Search", "Analytics", "Reading Goals", "Book Reviews"])

if page == "Dashboard":
    # Header with animated gradient
    st.markdown("""
        <div class='main-header'>
            <h1 style='font-size: 2.5rem; margin-bottom: 1rem;'>📚 Personal Library Dashboard</h1>
            <p style='font-size: 1.2rem; opacity: 0.9;'>Manage your book collection with style</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Statistics with enhanced metrics
    total_books = len(st.session_state.books)
    read_books = len([b for b in st.session_state.books if b['read_status']])
    unread_books = total_books - read_books
    favorite_books = len([b for b in st.session_state.books if b['id'] in st.session_state.favorites])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class='metric-card'>
                <div class='metric-value'>{}</div>
                <div class='metric-label'>Total Books</div>
            </div>
        """.format(total_books), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class='metric-card'>
                <div class='metric-value'>{}</div>
                <div class='metric-label'>Read Books</div>
            </div>
        """.format(read_books), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class='metric-card'>
                <div class='metric-value'>{}</div>
                <div class='metric-label'>Unread Books</div>
            </div>
        """.format(unread_books), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div class='metric-card'>
                <div class='metric-value'>{}</div>
                <div class='metric-label'>Favorite Books</div>
            </div>
        """.format(favorite_books), unsafe_allow_html=True)
    
    # Reading Progress
    if total_books > 0:
        progress = read_books / total_books
        st.markdown("""
            <div class='card'>
                <h3 style='margin-bottom: 1rem;'>Reading Progress</h3>
                <div style='background: #E5E7EB; height: 10px; border-radius: 5px; overflow: hidden;'>
                    <div style='background: linear-gradient(90deg, #7C3AED, #10B981); width: {}%; height: 100%;'></div>
                </div>
                <p style='text-align: center; margin-top: 0.5rem;'>{:.1f}% Complete</p>
            </div>
        """.format(progress * 100, progress * 100), unsafe_allow_html=True)
    
    # Recent Books with enhanced display
    st.markdown("### 📖 Recent Additions")
    if st.session_state.books:
        recent_books = sorted(st.session_state.books, key=lambda x: x['date_added'], reverse=True)[:6]
        st.markdown("<div class='book-grid'>", unsafe_allow_html=True)
        for book in recent_books:
            is_favorite = book['id'] in st.session_state.favorites
            st.markdown(f"""
                <div class='book-card'>
                    <img src='{book.get('cover_url', 'https://via.placeholder.com/300x200.png?text=No+Cover')}' class='book-cover'>
                    <div class='book-info'>
                        <div class='book-title'>{book['title']}</div>
                        <div class='book-author'>by {book['author']}</div>
                        <div style='display: flex; justify-content: space-between; align-items: center; margin-top: 1rem;'>
                            <div class='book-status status-{"read" if book["read_status"] else "unread"}'>
                                {"Read" if book["read_status"] else "Unread"}
                            </div>
                            <span class='favorite' style='color: {"#F59E0B" if is_favorite else "#E5E7EB"}; cursor: pointer;'>
                                {"★" if is_favorite else "☆"}
                            </span>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("No books in your library yet. Add some books to get started!")

elif page == "Add Books":
    st.markdown("""
        <div class='main-header'>
            <h1 style='font-size: 2.5rem; margin-bottom: 1rem;'>📚 Add New Books</h1>
            <p style='font-size: 1.2rem; opacity: 0.9;'>Expand your library collection</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("add_book_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Book Title")
            author = st.text_input("Author")
            pub_year = st.number_input("Publication Year", min_value=1000, max_value=datetime.now().year, value=2000)
        
        with col2:
            genre = st.selectbox("Genre", [
                "Islamic", "Science Fiction", "Mystery",
                "Romance", "Biography", "History", "Science", "Technology",
                "Fantasy", "Horror", "Poetry", "Drama", "Other"
            ])
            read_status = st.selectbox("Reading Status", ["Read", "Unread"])
            cover_url = st.text_input("Cover Image URL (optional)")
        
        # Additional fields
        st.markdown("### Additional Details")
        col3, col4 = st.columns(2)
        
        with col3:
            rating = st.slider("Rating (1-5)", 1, 5, 3)
            pages = st.number_input("Number of Pages", min_value=1, value=300)
        
        with col4:
            language = st.selectbox("Language", ["English", "Urdu", "Arabic", "Other"])
            format_type = st.selectbox("Format", ["Paperback", "Hardcover", "E-book", "Audiobook"])
        
        notes = st.text_area("Notes (optional)")
        
        if st.form_submit_button("Add Book"):
            if title and author:
                book = {
                    'id': st.session_state.current_id,
                    'title': title,
                    'author': author,
                    'publication_year': pub_year,
                    'genre': genre,
                    'read_status': read_status == "Read",
                    'cover_url': cover_url if cover_url else None,
                    'date_added': datetime.now().strftime("%Y-%m-%d"),
                    'rating': rating,
                    'pages': pages,
                    'language': language,
                    'format': format_type,
                    'notes': notes
                }
                st.session_state.books.append(book)
                st.session_state.current_id += 1
                save_books()
                st.success("Book added successfully!")
            else:
                st.error("Please fill in at least the title and author.")

elif page == "Manage Books":
    st.markdown("""
        <div class='main-header'>
            <h1 style='font-size: 2.5rem; margin-bottom: 1rem;'>📚 Manage Books</h1>
            <p style='font-size: 1.2rem; opacity: 0.9;'>Update and organize your collection</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.books:
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_genre = st.selectbox("Filter by Genre", ["All"] + list(set(b['genre'] for b in st.session_state.books)))
        with col2:
            filter_status = st.selectbox("Filter by Status", ["All", "Read", "Unread"])
        with col3:
            filter_rating = st.selectbox("Filter by Rating", ["All"] + [str(i) for i in range(1, 6)])
        
        # Apply filters
        filtered_books = st.session_state.books
        if filter_genre != "All":
            filtered_books = [b for b in filtered_books if b['genre'] == filter_genre]
        if filter_status != "All":
            filtered_books = [b for b in filtered_books if b['read_status'] == (filter_status == "Read")]
        if filter_rating != "All":
            filtered_books = [b for b in filtered_books if str(b['rating']) == filter_rating]
        
        # Display filtered books
        for book in filtered_books:
            with st.expander(f"{book['title']} by {book['author']}", expanded=False):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"""
                        <div class='card'>
                            <h3>{book['title']}</h3>
                            <p>Author: {book['author']}<br>
                            Genre: {book['genre']}<br>
                            Status: {"Read" if book['read_status'] else "Unread"}<br>
                            Rating: {"★" * book.get('rating', 0)}{"☆" * (5-book.get('rating', 0))}<br>
                            Pages: {book.get('pages', 'N/A')}<br>
                            Format: {book.get('format', 'N/A')}<br>
                            Language: {book.get('language', 'N/A')}</p>
                            {f"<p><strong>Notes:</strong> {book['notes']}</p>" if book.get('notes') else ""}
                        </div>
                    """, unsafe_allow_html=True)
                with col2:
                    if not book['read_status']:
                        if st.button("Mark as Read", key=f"read_{book['id']}"):
                            book['read_status'] = True
                            save_books()
                            st.success("Book marked as read!")
                            st.rerun()
                    
                    if st.button("Toggle Favorite", key=f"fav_{book['id']}"):
                        if book['id'] in st.session_state.favorites:
                            st.session_state.favorites.remove(book['id'])
                        else:
                            st.session_state.favorites.add(book['id'])
                        st.rerun()
                    
                    if st.button("Delete", key=f"delete_{book['id']}"):
                        st.session_state.books.remove(book)
                        save_books()
                        st.success("Book deleted!")
                        st.rerun()
    else:
        st.info("No books in your library yet. Add some books to get started!")

elif page == "Search":
    st.markdown("""
        <div class='main-header'>
            <h1 style='font-size: 2.5rem; margin-bottom: 1rem;'>🔍 Search Books</h1>
            <p style='font-size: 1.2rem; opacity: 0.9;'>Find books in your collection</p>
        </div>
    """, unsafe_allow_html=True)
    
    search_col1, search_col2 = st.columns([3, 1])
    with search_col1:
        search_query = st.text_input("Search by title, author, or genre")
    with search_col2:
        search_type = st.selectbox("Search in", ["All", "Title", "Author", "Genre"])
    
    if search_query:
        results = []
        search_query = search_query.lower()
        
        for book in st.session_state.books:
            if search_type == "All":
                if (search_query in book['title'].lower() or
                    search_query in book['author'].lower() or
                    search_query in book['genre'].lower()):
                    results.append(book)
            elif search_type == "Title" and search_query in book['title'].lower():
                results.append(book)
            elif search_type == "Author" and search_query in book['author'].lower():
                results.append(book)
            elif search_type == "Genre" and search_query in book['genre'].lower():
                results.append(book)
        
        if results:
            st.markdown("<div class='book-grid'>", unsafe_allow_html=True)
            for book in results:
                is_favorite = book['id'] in st.session_state.favorites
                st.markdown(f"""
                    <div class='book-card'>
                        <img src='{book.get('cover_url', 'https://via.placeholder.com/300x200.png?text=No+Cover')}' class='book-cover'>
                        <div class='book-info'>
                            <div class='book-title'>{book['title']}</div>
                            <div class='book-author'>by {book['author']}</div>
                            <div style='display: flex; justify-content: space-between; align-items: center; margin-top: 1rem;'>
                                <div class='book-status status-{"read" if book["read_status"] else "unread"}'>
                                    {"Read" if book["read_status"] else "Unread"}
                                </div>
                                <span class='favorite' style='color: {"#F59E0B" if is_favorite else "#E5E7EB"}; cursor: pointer;'>
                                    {"★" if is_favorite else "☆"}
                                </span>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("No books found matching your search criteria.")

elif page == "Analytics":
    st.markdown("""
        <div class='main-header'>
            <h1 style='font-size: 2.5rem; margin-bottom: 1rem;'>📊 Library Analytics</h1>
            <p style='font-size: 1.2rem; opacity: 0.9;'>Insights about your reading habits</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.books:
        # Create DataFrame
        df = pd.DataFrame(st.session_state.books)
        
        # Reading Progress
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("Reading Progress")
            fig = go.Figure(data=[go.Pie(
                labels=['Read', 'Unread'],
                values=[len(df[df['read_status']==True]), len(df[df['read_status']==False])],
                hole=.3,
                marker_colors=['#10B981', '#F59E0B']
            )])
            fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("Books by Genre")
            genre_counts = df['genre'].value_counts()
            fig = go.Figure(data=[go.Bar(
                x=genre_counts.values,
                y=genre_counts.index,
                orientation='h',
                marker_color='#7C3AED'
            )])
            fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Reading Timeline
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Books Added Over Time")
        df['date_added'] = pd.to_datetime(df['date_added'])
        timeline_data = df.groupby('date_added').size().reset_index(name='count')
        fig = px.line(timeline_data, x='date_added', y='count', 
                     title='Books Added Over Time',
                     line_shape="spline")
        fig.update_traces(line_color='#7C3AED')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Publication Year Distribution
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Publication Year Distribution")
        fig = px.histogram(df, x='publication_year', nbins=20,
                          title='Distribution of Book Publication Years')
        fig.update_traces(marker_color='#7C3AED')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Rating Distribution
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Rating Distribution")
        # Add default rating of 0 for books without ratings
        df['rating'] = df['rating'].fillna(0)
        rating_counts = df['rating'].value_counts().sort_index()
        fig = go.Figure(data=[go.Bar(
            x=rating_counts.index,
            y=rating_counts.values,
            marker_color='#7C3AED'
        )])
        fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    else:
        st.info("Add some books to see analytics!")

elif page == "Reading Goals":
    st.markdown("""
        <div class='main-header'>
            <h1 style='font-size: 2.5rem; margin-bottom: 1rem;'>💢 Reading Goals</h1>
            <p style='font-size: 1.2rem; opacity: 0.9;'>Track your reading progress</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Set Reading Goal")
        st.session_state.reading_goal = st.number_input(
            "Number of books to read this year",
            min_value=0,
            value=st.session_state.reading_goal
        )
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Current Progress")
        read_this_year = len([b for b in st.session_state.books 
                            if b['read_status'] and 
                            datetime.strptime(b['date_added'], "%Y-%m-%d").year == datetime.now().year])
        if st.session_state.reading_goal > 0:
            progress = min(read_this_year / st.session_state.reading_goal, 1)
            st.markdown(f"""
                <div style='text-align: center;'>
                    <h3>{read_this_year} / {st.session_state.reading_goal} Books</h3>
                    <div style='background: #E5E7EB; height: 10px; border-radius: 5px; overflow: hidden;'>
                        <div style='background: linear-gradient(90deg, #7C3AED, #10B981); width: {progress*100}%; height: 100%;'></div>
                    </div>
                    <p style='margin-top: 0.5rem;'>{progress*100:.1f}% Complete</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Set a reading goal to track your progress!")
        st.markdown("</div>", unsafe_allow_html=True)

elif page == "Book Reviews":
    st.markdown("""
        <div class='main-header'>
            <h1 style='font-size: 2.5rem; margin-bottom: 1rem;'>📝 Book Reviews</h1>
            <p style='font-size: 1.2rem; opacity: 0.9;'>Share your thoughts about books</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.books:
        book_to_review = st.selectbox(
            "Select a book to review",
            [f"{b['title']} by {b['author']}" for b in st.session_state.books]
        )
        
        if book_to_review:
            book = next(b for b in st.session_state.books 
                       if f"{b['title']} by {b['author']}" == book_to_review)
            
            with st.form("review_form"):
                rating = st.slider("Rating (1-5)", 1, 5, book.get('rating', 3))
                review = st.text_area("Your Review")
                
                if st.form_submit_button("Submit Review"):
                    book['rating'] = rating
                    book['review'] = review
                    save_books()
                    st.success("Review submitted successfully!")
            
            if 'review' in book:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.subheader("Your Review")
                st.markdown(f"Rating: {'★' * book['rating']}{'☆' * (5-book['rating'])}")
                st.markdown(book['review'])
                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("Add some books to write reviews!") 