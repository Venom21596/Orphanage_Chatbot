from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from intent_data import training_data

texts = [item[0] for item in training_data]
labels = [item[1] for item in training_data]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)
model = MultinomialNB()
model.fit(X, labels)


def predict_intent(user_text):
    vect = vectorizer.transform([user_text])
    probabilities = model.predict_proba(vect)[0]
    max_prob = max(probabilities)
    predicted_label = model.classes_[probabilities.argmax()]
    if max_prob < 0.60:
        return "unknown"
    return predicted_label


app = Flask(__name__)
CORS(app)

responses = {
    "start": {
        "message": "Welcome to Sneha Jyothi Orphan Children's Home \U0001f499 How can I help you?",
        "options": ["About Us", "What We Do", "Donate", "Volunteer", "Contact Info", "Restart Chatbot"]
    },
    "main_menu": {
        "options": ["About Us", "What We Do", "Donate", "Volunteer", "Contact Info", "Restart Chatbot"]
    },
    "About Us": {
        "message": (
            "Sneha Jyothi Orphan Children\u2019s Home was established in 2010 near Bangalore. "
            "We provide a safe and loving home for orphaned and vulnerable children, "
            "along with education, food, healthcare, and emotional care."
        ),
        "options": ["Back"]
    },
    "What We Do": {
        "message": (
            "We support children through:\n"
            "\u2022 Education and schooling\n"
            "\u2022 Nutritious meals\n"
            "\u2022 Safe shelter\n"
            "\u2022 Healthcare services\n"
            "\u2022 Emotional and moral support"
        ),
        "options": ["Back"]
    },
    "Donate": {
        "message": "How would you like to contribute?",
        "options": ["Donate Money", "Donate Food", "Donate Clothes", "Back"]
    },
    "Donate Money": {
        "message": (
            "\U0001f3e6 Bank Transfer Details:\n"
            "Account Name: Sneha Jyothi Orphan Children\u2019s Home\n"
            "Account Number: 3812 0011 0004 578\n"
            "Bank: Canara Bank, Bangalore\n"
            "IFSC Code: CNRB0003812\n"
            "Account Type: Savings\n\n"
            "\U0001f4f1 UPI / Google Pay:\n"
            "UPI ID: sneha.jyothi@canara\n"
            "Phone Pay / GPay: +91-9448164099\n\n"
            "\U0001f4dc 80G Tax Exemption available \u2014 a receipt will be issued for all donations.\n"
            "Please WhatsApp your transaction screenshot to +91-9448164099 for confirmation."
        ),
        "options": ["Back"]
    },
    "Donate Food": {
        "message": (
            "\U0001f35b We gratefully accept the following:\n"
            "\u2022 Dry goods: Rice, dal, wheat flour, cooking oil, sugar, salt\n"
            "\u2022 Fresh produce: Vegetables, fruits, milk\n"
            "\u2022 Packaged foods: Biscuits, snacks (within expiry)\n"
            "\u2022 Cooked meals: For special occasions / events\n\n"
            "\u23f0 Drop-off Timings:\n"
            "Monday \u2013 Saturday: 9:00 AM \u2013 6:00 PM\n"
            "Sunday: 10:00 AM \u2013 2:00 PM\n\n"
            "\U0001f4cd Drop-off Address:\n"
            "Sneha Jyothi Orphan Children\u2019s Home,\n"
            "No. 14, 3rd Cross, Judicial Layout,\n"
            "Kengeri, Bangalore \u2013 560060\n\n"
            "\u26a0\ufe0f Please call ahead before visiting: +91-9448164099"
        ),
        "options": ["Back"]
    },
    "Donate Clothes": {
        "message": (
            "\U0001f455 Clothing Donation Guidelines:\n\n"
            "\u2705 We accept:\n"
            "\u2022 Clean, washed clothes in good condition\n"
            "\u2022 Boys & girls clothing (ages 3\u201317 years)\n"
            "\u2022 School uniforms, casual wear, nightwear\n"
            "\u2022 Footwear (sandals, shoes \u2013 sizes 3 to 9)\n"
            "\u2022 Seasonal wear: Sweaters, raincoats\n\n"
            "\u274c Please do not donate:\n"
            "\u2022 Torn, stained, or heavily worn items\n"
            "\u2022 Adult clothing (unless for staff use)\n\n"
            "\U0001f4cd Drop-off Address:\n"
            "Sneha Jyothi Orphan Children\u2019s Home,\n"
            "No. 14, 3rd Cross, Judicial Layout,\n"
            "Kengeri, Bangalore \u2013 560060\n\n"
            "\u23f0 Timings: Mon\u2013Sat 9 AM \u2013 6 PM\n"
            "Call us: +91-9448164099"
        ),
        "options": ["Back"]
    },
    "Volunteer": {
        "message": (
            "\U0001f91d We\u2019d love to have you with us! Here\u2019s how you can volunteer:\n\n"
            "\U0001f4da Roles Available:\n"
            "\u2022 Teaching (English, Math, Science, Arts & Crafts)\n"
            "\u2022 Mentoring & career guidance (for older children)\n"
            "\u2022 Sports coaching & physical activities\n"
            "\u2022 Medical / health check-up camps (doctors & nurses welcome)\n"
            "\u2022 Event planning & festival celebrations\n"
            "\u2022 Photography, music, or skill-based workshops\n\n"
            "\U0001f4cb How to Register:\n"
            "1\ufe0f\u20e3 Call or WhatsApp: +91-9448164099\n"
            "2\ufe0f\u20e3 Email us: murthytg.2011@gmail.com\n"
            "3\ufe0f\u20e3 Share your name, availability & area of interest\n"
            "4\ufe0f\u20e3 We\u2019ll schedule an orientation visit\n\n"
            "\u23f0 Volunteering Hours:\n"
            "Monday \u2013 Saturday: 9:00 AM \u2013 5:00 PM\n"
            "Weekend slots also available on request\n\n"
            "\u2728 Even a single day makes a difference. All backgrounds welcome!"
        ),
        "options": ["Back"]
    },
    "Contact Info": {
        "message": (
            "\U0001f4cd Locations: Bangalore & Mysore\n"
            "\U0001f4de Phone: +91-8022747070, +91-9448164099\n"
            "\u2709\ufe0f Email: murthytg.2011@gmail.com"
        ),
        "options": ["Back"]
    },
    "Restart Chatbot": {
        "message": "Chatbot restarted \U0001f504",
        "options": []
    }
}


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    if user_message in ("start", "Restart Chatbot"):
        return jsonify(responses["start"])

    if user_message == "Back":
        return jsonify(responses["main_menu"])

    if user_message in responses:
        return jsonify(responses[user_message])

    predicted_intent = predict_intent(user_message)
    intent_map = {
        "donate": "Donate",
        "volunteer": "Volunteer",
        "about": "About Us",
        "what_we_do": "What We Do",
        "contact": "Contact Info"
    }

    if predicted_intent != "unknown" and predicted_intent in intent_map:
        mapped_option = intent_map[predicted_intent]
        if mapped_option in responses:
            return jsonify(responses[mapped_option])

    return jsonify({
        "message": "Sorry, I couldn\u2019t understand that. Please choose an option from the menu.",
        "options": ["Back"]
    })


if __name__ == "__main__":
    app.run(debug=True)