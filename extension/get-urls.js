console.log("getting-urls");

// Flag to check if listeners have been added
let listenersAdded = false;

function addEventListeners() {
  if (listenersAdded) return;
  listenersAdded = true;

  // Add an event listener for tab updates
  chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.url && !changeInfo.url.startsWith("chrome://")) {
      console.log(`Tab ID ${tabId} URL updated to: ${changeInfo.url}`);
      updateAndLogTabUrls();
    }
  });

  // Add an event listener for tab removal
  chrome.tabs.onRemoved.addListener((tabId) => {
    console.log(`Tab ID ${tabId} closed.`);
    updateAndLogTabUrls();
  });
}

// Initialize an array to store URLs of open tabs
let openTabUrls = [];

// Function to query and update the array of URLs of all open tabs, excluding chrome:// URLs
function updateAndLogTabUrls() {
  console.clear();
  console.log("Updating and logging URLs...");

  chrome.tabs.query({}, function(tabs) {
    openTabUrls = tabs.filter(tab => !tab.url.startsWith("chrome://")).map(tab => tab.url);
    console.log("Current open tabs (excluding chrome:// URLs):");
    openTabUrls.forEach(url => console.log(url));

    // Send the URLs to the Flask server
    sendUrlsToServer(openTabUrls);
  });
}

// Function to send URLs to the Flask server
function sendUrlsToServer(urls) {
  fetch('http://localhost:5000/api/save-urls', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({urls: urls}),
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => console.log('Success:', data))
  .catch((error) => {
    console.error('Error:', error);
  });
}

// Initially update and log URLs of all open tabs, excluding chrome:// URLs
updateAndLogTabUrls();

// Add event listeners for tab updates and removals
addEventListeners();
