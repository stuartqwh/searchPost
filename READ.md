Auto search eBay Post to Facebook page.

1. The user enters a query and category ID in the appropriate entry fields.
2. The user clicks the "Search" button, which triggers the `get_search_results` function to fetch search results from eBay using the Graph API.
3. The search results are displayed in the listbox.
4. The user selects an item from the listbox by clicking on it.
5. The user clicks the "Show Image" button, which triggers the `show_image` function to display the selected item's thumbnail image.
6. The user enters a description for the item in the text entry field below the image.
7. The user clicks the "Post to Facebook" button, which triggers the `post_to_facebook` function to post the selected item to Facebook using the Graph API.
8. The script displays a success message upon successful posting and removes it after 5 seconds.
9. The user can exit the program by clicking the "Exit" button.

The script uses the `gemToken` library to authenticate with eBay and the `facebook-sdk` library to post to Facebook using the Graph API. The script also uses Tkinter to create a user 
interface for searching and posting items to Facebook.

Text generated with codellama