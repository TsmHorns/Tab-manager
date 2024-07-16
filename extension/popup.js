document.addEventListener('DOMContentLoaded', async () => {
  try {
    // Query all active Google tabs
    const tabs = await chrome.tabs.query({
      url: [
        '*://*.google.com/*'
      ]
    });

    const template = document.getElementById('li_template');
    const elements = new Set();

    for (const tab of tabs) {
      const element = template.content.firstElementChild.cloneNode(true);
      const title = tab.title || "No title";
      const url = tab.url;

      element.querySelector('.title').textContent = title;
      element.querySelector('.url').textContent = url;
      element.querySelector('a').href = url;
      element.querySelector('a').target = "_blank";

      elements.add(element);
    }

    document.querySelector('ul').append(...elements);

    const button = document.querySelector('button');
    button.addEventListener('click', async () => {
      const tabIds = tabs.map(({ id }) => id);
      if (tabIds.length) {
        const group = await chrome.tabs.group({ tabIds });
        await chrome.tabGroups.update(group, { title: 'Google Tabs' });
      }
    });
  } catch (error) {
    console.error('Failed to load tabs:', error);
  }
});
