# Readwise Add-on For Anki

## Installation
### Manual Installation
1. Download Add-on: Clone this GitHub repository to your local machine.
```
git clone https://github.com/mattbarlow-sg/readwise-anki.git
```
2. Locate Anki Add-ons Folder:
- Windows: C:\Users\[Your Username]\AppData\Roaming\Anki2\addons21\
- Mac: ~/Library/Application Support/Anki2/addons21/
- Linux: ~/.local/share/Anki2/addons21/
3. Copy Add-on: Copy the add-on folder (readwise-anki) to your Anki addons21 directory.
4. Restart Anki: Close and reopen Anki to complete the installation. The new features should now be available.
5. Set your Readwise API Key: Click on Tools -> Add-ons. Double click the readwise-anki extension. Add your `readwiseApiKey`. Get your Readwise API token [here](https://readwise.io/access_token).

## Usage
Click on Tools -> Sync Readwise Reader. This will create a new deck called Articles. Click Study Now on the deck, read articles, and advance the cards in the deck.

As you finish articles, archive them in Readwise Reader.

When you are finished with your study session, click Tools -> Sync Readwise Reader again, and the articles you archived will be removed from the deck.

See a [demo](https://www.loom.com/share/d3039f29a9d34542acb6c501f04da1af).
