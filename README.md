# Flash_cards_LearningFrenchVocabs
A simple flashcard app built with Python and Tkinter to help users learn French vocabulary in an interactive way.

Features
- Displays French words with English translations.
- Automatically flips the card after 3 seconds to reveal the translation.
- Users can mark words they know or don't know.
- Words marked as known are removed from future sessions.
- Progress is saved automatically so you can pick up where you left off.

How this Flash_card code works:
1. The app displays a random French word.
2. After 3 seconds, the card flips to show the English translation.
Click:
✅ Right button if you know the word (it will be removed from future sessions).
❌ Wrong button if you don't know the word (it will stay in the learning list).
When you close the app, your progress is saved in words_to_learn.csv for next time.

How to Use:
1. Clone this repository
2. Make sure you have the following: A "data/french_words.csv" file containing your vocabulary.
3. All required images in the images folder.
4. Run the app: python main.py

Notes:
1. The app does not require any external API keys.
2. All user data (known/unknown words) is stored locally.
3. Customize: You can replace french_words.csv with your own vocabulary set (in the same format) to learn different words or languages.
