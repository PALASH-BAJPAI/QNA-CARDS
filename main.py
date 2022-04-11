from flask import Flask, render_template,jsonify, request,redirect, url_for,abort
from model import db, save_db
app = Flask(__name__)

# HOME PAGE 
@app.route('/')
def hello():
    return render_template('index.html', message='🎴')


#CARDS
@app.route('/card/<int:index>')
def card_view(index):
    card=db[index]
    return render_template('flashcards.html', card=card, index=index, max_index=len(db)-1)


#CARD API
@app.route('/api/cardlist')
def api_card_list():
    return jsonify(db)


#ADD CARD
@app.route('/add_card', methods=['GET','POST'])
def add_card():
    if request.method == 'POST':
        card={"question": request.form['question'], 
              "answer": request.form['answer']}
        db.append(card)
        save_db(db)
        return redirect(url_for('card_view', index=len(db)-1))
    else:
        return render_template('add_card.html')



#DELETE CARD
@app.route('/remove_card/<int:index>', methods=['GET','POST'])
def remove_card(index):
    try:
        if request.method == 'POST':
            del db[index]
            save_db(db)
            return redirect(url_for('hello'))
        else:
            return render_template('remove_card.html',card=db[index])
    except IndexError:
        abort(404)



if __name__ == '__main__':
    app.run(debug=True)
    
