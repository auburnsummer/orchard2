# Frontend-only work flow

## Requirements

 - **node.js**: The minimum version supported is 20, but you should probably
   install the latest LTS or release (24.15.0 or 25.9.0 at the time of writing)

## Getting Started

 1. Clone the repo:

    ```bash
    $ git clone https://github.com/auburnsummer/orchard2.git
    ```

 2. Move into the `client` directory:

    ```bash
    $ cd client
    ```

 3. Install dependencies:

    ```bash
    $ npm install
    ```

 4. Then start the dev server:

    ```bash
    $ npm run dev
    ```

 5. Go to `https://rhythm.cafe` and add a cookie with the key `_dev_client` and the value `1` (note the leading underscore.)
    You can do this in the 'Storage' tab of devtools in Firefox or the 'Application' tab of devtools in Chrome.

    Alternatively, you can set up the cookie by pasting this snippet into the browser's console:

    ```javascript
    document.cookie = "_dev_client=1; path=/";
    ```

 6. Refresh the page. You may see a prompt on screen asking for local network access. Grant the permission.

 7. rhythm.cafe is now talking to your local dev server. You can make edits and the changes should reflect on the page.

 8. Once you're done, delete the `_dev_client` cookie to return to normal.