import streamlit as st
import json
import os

data_file = 'library.txt'

def load_library():
    if os.path.exists(data_file):
        with open(data_file, 'r') as file:
            try:
                content = file.read().strip()
                if not content:
                    return []
                return json.loads(content)
            except json.JSONDecodeError:
                return []
    return []

def save_library(library):
    with open(data_file, 'w') as file:
        json.dump(library, file, indent=4)

def add_book(library):
    st.subheader('➕ Add a New Book')
    with st.form(key='add_book_form'):
        title = st.text_input('Enter the title of the book')
        author = st.text_input('Enter the author of the book')
        year = st.text_input('Enter the year of the book')
        genre = st.text_input('Enter the genre of the book')
        read = st.checkbox('Have you read the book?')
        submit = st.form_submit_button('Add Book')

        if submit:
            if title and author and year and genre:
                new_book = {
                    "title": title,
                    "author": author,
                    "year": year,
                    "genre": genre,
                    "read": read
                }
                library.append(new_book)
                save_library(library)
                st.success(f'✅ Book "{title}" added successfully.')
            else:
                st.error('❗Please fill all fields.')

def remove_book(library):
    st.subheader('🗑 Remove a Book')
    titles = [book['title'] for book in library]
    if titles:
        book_to_remove = st.selectbox('Select a book to remove', titles)
        if st.button('Remove Book'):
            library[:] = [book for book in library if book['title'] != book_to_remove]
            save_library(library)
            st.success(f'✅ Book "{book_to_remove}" removed successfully.')
    else:
        st.info('Library is empty. Nothing to remove.')

def search_book(library):
    st.subheader('🔎 Search a Book')
    search_by = st.selectbox('Search by', ['title', 'author'])
    search_term = st.text_input(f'Enter the {search_by}')

    if st.button('Search'):
        results = [book for book in library if search_term.lower() in book.get(search_by, '').lower()]
        if results:
            for book in results:
                status = '✅ Read' if book['read'] else '📖 Unread'
                st.write(f"**{book['title']}** by *{book['author']}* ({book['year']}) - {book['genre']} - {status}")
        else:
            st.warning(f'No books found for "{search_term}".')

def display_all_books(library):
    st.subheader('📚 All Books')
    if library:
        for book in library:
            status = '✅ Read' if book['read'] else '📖 Unread'
            st.write(f"**{book['title']}** by *{book['author']}* ({book['year']}) - {book['genre']} - {status}")
    else:
        st.info('The library is empty.')

def display_statistics(library):
    st.subheader('📈 Library Statistics')
    total_books = len(library)
    read_books = sum(1 for book in library if book['read'])
    percentage_read = (read_books / total_books) * 100 if total_books else 0

    st.metric('Total Books', total_books)
    st.metric('Books Read', read_books)
    st.metric('Percentage Read', f"{percentage_read:.2f}%")

def main():
    st.title('📖 Personal Library Manager')
    library = load_library()

    menu = ['Home', 'Add Book', 'Remove Book', 'Search Book', 'Display All Books', 'Display Statistics']
    choice = st.sidebar.selectbox('Navigation', menu)

    if choice == 'Home':
        st.write('Welcome to your **Personal Library Manager**! 📚\nManage your books easily.')
    elif choice == 'Add Book':
        add_book(library)
    elif choice == 'Remove Book':
        remove_book(library)
    elif choice == 'Search Book':
        search_book(library)
    elif choice == 'Display All Books':
        display_all_books(library)
    elif choice == 'Display Statistics':
        display_statistics(library)

if __name__ == '__main__':
    main()
