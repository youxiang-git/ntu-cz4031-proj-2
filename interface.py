from flask import Flask, render_template
app = Flask(__name__,
            template_folder='templates')

explanation = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Commodi laboriosam, doloremque, aspernatur expedita quisquam asperiores voluptatibus magni odio voluptatem recusandae sed et aliquam, inventore ducimus? Quos quae nisi sunt ex!'

@app.route('/')
def home():
    return render_template('index.html', explanation=explanation)

if __name__ == '__main__':
    app.run()
