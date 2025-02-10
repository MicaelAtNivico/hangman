from flask import Flask, render_template, request, session, redirect, url_for
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Setting up words for game
a = ["började", "använda", "behöver", "finns", "mellan", "genom", "eftersom", "därför", "alltid", "aldrig", "också", "vanligt", "viktigt", "roligt", "intressant", "svårt", "lätt", "stort", "litet", "gammalt", "ungt", "vackert", "fult", "snabbt", "långsamt", "högt", "lågt", "varmt", "kallt", "sött", "surt", "salt", "beskt", "mjukt", "hårt", "viktigt", "onödigt", "intressant", "tråkigt", "lätt", "svårt", "roligt", "allvarligt", "vänligt", "ovänligt", "snällt", "elakt", "dumt", "smart", "klokt", "vist", "galet", "lyckligt", "ledset", "argt", "rädd", "trött", "piggt", "hungrigt", "mätt", "törstigt", "fullt", "tomt", "helt", "trasigt", "rent", "smutsigt", "ljust", "mörkt", "tyst", "högljutt", "vilt", "tam", "fritt", "bundet", "rikt", "fattigt", "känt", "okänt", "viktigt", "oviktigt", "försöka", "förstå", "hjälpa", "behöva", "kunna", "vilja", "måste", "skulle", "borde", "verkligen", "faktiskt", "tyvärr", "antagligen", "förmodligen", "dessutom", "istället", "fortfarande", "tillsammans", "ensam", "själv", "andra", "olika", "samma", "egna", "vissa", "flesta", "båda", "ingen", "någon", "mycket", "lite", "mer", "mindre", "mest", "minst"]

# Setting up hangman art
row0 = ""
row7_1 = "HANGMAN (100 most common swedish words.. If you ask Gemini)"
row6_1 = "   ____"
row5_1 = "  |"
row5_2 = "  |/"
row5_3 = "  |/   |"
row4_1 = "  |"
row4_2 = "  |    O"
row3_1 = "  |"
row3_2 = "  |    |"
row3_3 = "  |   /|"
row3_4 = "  |   /|\\"
row2_1 = " / \\"
row2_2 = " / \\  /"
row2_3 = " / \\  / \\"
row1_1 = "/   \\"

# Setting up hangman art for each try
Shoot0 = f""" {row7_1}
{row0}
{row0}
{row0}
{row0}
{row0}
{row0}
"""

Shoot1 = f""" {row7_1}
{row0}
{row0}
{row0}
{row0}
{row2_1}
{row1_1}
"""

Shoot2 = f""" {row7_1}
{row0}
{row5_1}
{row4_1}
{row3_1}
{row2_1}
{row1_1}
"""

Shoot3 = f""" {row7_1}
{row6_1}
{row5_1}
{row4_1}
{row3_1}
{row2_1}
{row1_1}
"""

Shoot4 = f""" {row7_1}
{row6_1}
{row5_2}
{row4_1}
{row3_1}
{row2_1}
{row1_1}
"""

Shoot5 = f""" {row7_1}
{row6_1}
{row5_3}
{row4_1}
{row3_1}
{row2_1}
{row1_1}
"""

Shoot6 = f""" {row7_1}
{row6_1}
{row5_3}
{row4_2}
{row3_1}
{row2_1}
{row1_1}
"""

Shoot7 = f""" {row7_1}
{row6_1}
{row5_3}
{row4_2}
{row3_2}
{row2_1}
{row1_1}
"""

Shoot8 = f""" {row7_1}
{row6_1}
{row5_3}
{row4_2}
{row3_3}
{row2_1}
{row1_1}
"""

Shoot9 = f""" {row7_1}
{row6_1}
{row5_3}
{row4_2}
{row3_4}
{row2_1}
{row1_1}
"""

Shoot10 = f""" {row7_1}
{row6_1}
{row5_3}
{row4_2}
{row3_4}
{row2_2}
{row1_1}
"""

Shoot11 = f""" {row7_1}
{row6_1}
{row5_3}
{row4_2}
{row3_4}
{row2_3}
{row1_1}
GAME OVER"""

# Function to convert the word to hidden name
def ConvertLine(UsedChar, Word):
    CharLeft = 0
    HiddenName = ""
    i = 0
    while i < len(Word):
        if Word[i].lower() in UsedChar.lower():
            HiddenName = HiddenName + Word[i] + " "
        else:
            HiddenName = HiddenName + "_ "
            CharLeft += 1
        i += 1
    return HiddenName, CharLeft

# Main function
@app.route("/", methods=["GET", "POST"])
def index():
    if "word" not in session:
        session["word"] = random.choice(a)
        session["used_char"] = ""
        session["tries"] = 0

    hidden_name, char_left = ConvertLine(session["used_char"], session["word"])

    if request.method == "POST":
        x = request.form.get("guess")

        if x and len(x) == 1 and x.lower() not in session["used_char"]:
            session["used_char"] += x.lower() + ","
            if x.lower() not in session["word"].lower():
                session["tries"] += 1

        return redirect(url_for("index"))

    word = session["word"]
    used_char = session["used_char"]
    tries = session["tries"]

    if char_left == 0:
        result = "YOU SOLVED IT!"
    elif tries >= 11:
        result = f"GAME OVER. The word was: {word}"
    else:
        result = None

    return render_template("index.html",
                           hangman_art=globals()["Shoot" + str(tries)],
                           hidden_name=hidden_name,
                           used_char=used_char,
                           result=result,
                           word=word)


#Ready for new game. clering old session data
@app.route("/new_game")  
def new_game():
    session.clear()
    return redirect(url_for("index"))  

if __name__ == "__main__":
    app.run(debug=True)