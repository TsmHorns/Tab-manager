// background.js

chrome.runtime.onInstalled.addListener(() => {
  console.log('Extension installed');
});

chrome.tabs.onActivated.addListener(activeInfo => {
  console.log('Tab activated', activeInfo);
});

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && /^https:\/\/www\.google/.test(tab.url)) {
    console.log('Tab updated', tab);
  }
});
