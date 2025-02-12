import streamlit as st

def main():
    # Custom CSS for styling
    st.markdown(
        """
        <style>
        /* Remove default padding and margin */
        html, body, .stApp {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
        }

        /* Full-width background gradient */
        .stApp {
            background: linear-gradient(to right, #74ebd5, #acb6e5);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }

        /* Full-width output window */
        .output-window {
            background-color: #ffffff;
            padding: 20px;
            border: 1px solid #cccccc;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            width: 90%; /* Use 90% of the screen width */
            height: 300px; /* Increased height */
            overflow-y: auto;
            margin: 20px auto; /* Center alignment */
            text-align: left;
        }

        /* Full-width input section */
        .input-section {
            display: flex;
            gap: 10px;
            justify-content: center;
            align-items: center;
            margin-top: 20px;
            width: 90%; /* Use 90% of the screen width */
            margin-left: auto;
            margin-right: auto;
        }

        /* Input box styling */
        .input-box {
            flex-grow: 1;
            background-color: #ffffff;
            padding: 10px;
            border: 1px solid #cccccc;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }

        /* Submit button styling */
        .submit-button {
            background-color: #00698f;
            color: #ffffff;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        }

        .submit-button:hover {
            background-color: #003d5c;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Title Section
    st.markdown("<h1 style='text-align: center; font-size: 50px; color: #003d5c;'>Invisible Disability Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 20px; color: #444;'>Nairobi Disability Support Platform</p>", unsafe_allow_html=True)

    # Output Window
    output_window = st.empty()  # Placeholder for dynamic output
    with output_window.container():
        st.markdown("<div class='output-window'>Output will be displayed here...</div>", unsafe_allow_html=True)

    # Input and Submit Button Section
    st.markdown(
        """
        <div class="input-section">
            <input class="input-box" placeholder="Type your query here" id="input-field"></input>
            <button class="submit-button" onclick="submitQuery()">Submit</button>
        </div>
        <script>
        function submitQuery() {
            const inputField = document.getElementById('input-field');
            const query = inputField.value;
            if (query.trim() !== '') {
                // Pass query to Streamlit via WebSocket
                Streamlit.setComponentValue(query);
                inputField.value = ''; // Clear input box
            } else {
                alert("Please enter a query!");
            }
        }
        </script>
        """,
        unsafe_allow_html=True,
    )

    # Handle Submission
    if "query" in st.session_state:
        query = st.session_state.query
        if query:
            output_window.markdown(f"<div class='output-window'>{query}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()