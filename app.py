from flask import Flask,render_template,request
from tool1 import rate_all
app=Flask(__name__)
@app.route('/',methods=['GET','POST'])
def home():
    if request.method=='POST':
        jb_path=request.form['jb_path']
        resume_path=request.form['resume_path']
        ck_path=request.form['ck_path']
        rating_saving_path=request.form['rating_save_path']
        rating=rate_all(jb_content_path=jb_path,
                    resume_group_path=resume_path,
                    critical_keyword_path=ck_path,
                    rating_saving_path=rating_saving_path)
        return render_template('display_rating.html',info=rating,name='sajan')
    else:
        return render_template('index.html')
if __name__=='__main__':
    app.run(debug=True)