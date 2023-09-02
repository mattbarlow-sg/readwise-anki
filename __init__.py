from aqt import mw
from aqt.utils import showInfo, qconnect
from anki.sync import AnkiRequestsClient
from aqt.qt import QAction
import json
import hashlib

def create_card(title: str, url: str) -> None:
    if title is None or url is None:
        return

    config = mw.addonManager.getConfig(__name__)
    noteTypeName = config.get("noteTypeName")
    readwiseArticleDeck = config.get("readwiseArticleDeck")
    model = mw.col.models.by_name(noteTypeName)

    deck_id = mw.col.decks.id(readwiseArticleDeck)

    url_hash = hashlib.sha1(url.encode()).hexdigest()
    note_id_list = mw.col.find_notes(f'UrlHash:"{url_hash}"')

    if len(note_id_list) == 0:
        note = mw.col.newNote({'mid': model['id'], 'did': deck_id})
        note['Front'] = title
        note['Url'] = url
        note['UrlHash'] = url_hash
        mw.col.add_note(note, deck_id)
        mw.col.reset()

def sync_archive(item_dict) -> None:
    config = mw.addonManager.getConfig(__name__)
    readwiseArticleDeck = config.get("readwiseArticleDeck")
    deck_id = mw.col.decks.id(readwiseArticleDeck)

    print(f"Working on deck: {readwiseArticleDeck}, id: {deck_id}")

    deck_note_ids = mw.col.decks.cids(deck_id)
    notes_to_delete = []

    for note_id in deck_note_ids:
        if not mw.col.find_notes(f"nid:{note_id}"):
            print(f"Note {note_id} does not exist in the database.")
            continue

        note = mw.col.get_note(note_id)
        url = note.fields[1]  # Adjust the index based on your note type
        item = item_dict.get(url)

        if item and item['location'] == 'archive':
            print(f"Marked for deletion: Note id {note_id}, url: {url}")
            notes_to_delete.append(note_id)

    for note_id in notes_to_delete:
        print(f"Deleting note: {note_id}")
        mw.col.remove_notes([note_id])

def make_request(pageCursor=None) -> None:
    config = mw.addonManager.getConfig(__name__)
    readwiseApiKey = config.get("readwiseApiKey")
    client = AnkiRequestsClient()

    url = "https://readwise.io/api/v3/list/"
    if pageCursor:
        url += f"?pageCursor={pageCursor}"

    response = client.get(
        url,
        headers={"Authorization": f'Token {readwiseApiKey}'}
    )

    if response.status_code == 200:
        on_result_ready(response.text)

        data = json.loads(response.text)
        next_page_cursor = data.get("nextPageCursor")
        if next_page_cursor:
            make_request(pageCursor=next_page_cursor)
        else:
            mw.reset()
            showInfo("Sync Complete!")
    else:
        print(f"Request failed with status code {response.status_code}")


def on_result_ready(response) -> None:
    data = json.loads(response)
    item_dict = {item['url']: item for item in data['results']}
    for url, item in item_dict.items():
        if item['location'] != 'archive':
            create_card(item['title'], url)

    sync_archive(item_dict)

action = QAction("Sync Readwise Reader", mw)
qconnect(action.triggered, make_request)
mw.form.menuTools.addAction(action)
