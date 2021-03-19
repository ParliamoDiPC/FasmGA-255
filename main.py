from flask import Flask, render_template, request, redirect, send_from_directory
from replit import db
import random, string, os

url = "https://255.fasm.ga/"
siteName = "Fasm.ga | 255"

app = Flask('app')

def newString():
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(25))
    return result_str

def getStrings(id):
    urls = db["user_id_" + id]
    return urls

def compileLine(id):
    return '<tr><td>' + id[5:] + '</td><td>' + db["name_" + id[5:]] + '</td><td>' + '<a href ="https://255.fasm.ga/delete/' + id[5:] + '"><i class="material-icons" style="color:#1E1E1E">delete</i></a>      <a href ="https://255.fasm.ga/edit/' + id[5:] + '"><i class="material-icons"style="color:#1E1E1E">edit</i></a></td></tr>'

@app.route('/')
def index():
    global siteName
    if request.headers['X-Replit-User-Id']:
        return render_template("submit.html", siteName = siteName, user_name=request.headers['X-Replit-User-Name'])
    else:
        return render_template("index.html", siteName=siteName)

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static"), "favicon.ico")

@app.route('/wp-login.php')
def wploginphp():
    global siteName
    if request.headers['X-Replit-User-Id']:
        return redirect(url + 'dashboard')
    else:
        return redirect("/", 302)

@app.route('/dashboard')
def dashboard():
    global siteName
    if request.headers['X-Replit-User-Id']:
        idTable = ""
        try:
            ids = getStrings(request.headers['X-Replit-User-Id'])
            for id in ids:
                idTable = idTable + compileLine(id)
            if idTable == "":
                return render_template('dashboard.html', siteName=siteName, user_id=request.headers['X-Replit-User-Id'], user_name=request.headers['X-Replit-User-Name'], user_roles=request.headers['X-Replit-User-Roles'], idTable = idTable, error = "<center><h6 style='color:#ffffff'>Non hai ancora creato una nota.</h6></center>")
            return render_template('dashboard.html',siteName=siteName, user_id=request.headers['X-Replit-User-Id'],user_name=request.headers['X-Replit-User-Name'], user_roles=request.headers['X-Replit-User-Roles'],idTable = idTable,error = "")
        except:
            return render_template('dashboard.html', siteName=siteName, user_id=request.headers['X-Replit-User-Id'], user_name=request.headers['X-Replit-User-Name'], user_roles=request.headers['X-Replit-User-Roles'], idTable = idTable, error = "<center><h6 style='color:#ffffff'>Non hai ancora creato una nota.</h6></center>")
    else:
        return redirect("/", 302)

@app.route('/delete/<string:id>')
def delete(id):
    if request.headers["X-Replit-User-Id"]:
        global siteName
        if not id:
            id = "Please stop trying to break the site lol"
        return render_template('delete.html', siteName=siteName, user_id=request.headers['X-Replit-User-Id'], user_name=request.headers['X-Replit-User-Name'], user_roles=request.headers['X-Replit-User-Roles'], id = id)
    else:
        return redirect("/", 302)

@app.route('/delete/<string:id>/')
def delete2(id):
    if request.headers["X-Replit-User-Id"]:
        global siteName
        if not id:
            id = "Please stop trying to break the site lol"
        return render_template('delete.html', siteName=siteName, user_id=request.headers['X-Replit-User-Id'], user_name=request.headers['X-Replit-User-Name'], user_roles=request.headers['X-Replit-User-Roles'], id = id)
    else:
        return redirect("/", 302)

@app.route('/edit/<string:id>')
def edit(id):
	if request.headers["X-Replit-User-Id"]:
		global siteName
		return render_template('edit.html', siteName=siteName, user_id = request.headers['X-Replit-User-Id'], user_name = request.headers['X-Replit-User-Name'], user_roles=request.headers['X-Replit-User-Roles'], oldNote = db["note_" + id], oldDescription = db["description_" + id], id = id)
	else:
		return redirect("/", 302)

@app.route('/edit/<string:id>/')
def edit2():
	id = request.form["id"]
	if request.headers["X-Replit-User-Id"]:
		global siteName
		return render_template('edit.html', siteName=siteName, user_id=request.headers['X-Replit-User-Id'], user_name=request.headers['X-Replit-User-Name'], user_roles=request.headers['X-Replit-User-Roles'], oldNote = db["note_" + id], oldDescription = db["description_" + id], id=id)
	else:
		return redirect("/", 302)

@app.route('/del', methods=['POST'])
def deleteEntry():
	id = request.form["id"]
	global siteName
	if len(request.headers['X-Replit-User-Id']) != 0:
		user_id = request.headers['X-Replit-User-Id']
		users_ids = db["user_id_" + user_id]
		try:
			users_ids.remove("note_" + id)
			del db["note_" + id]
			del db["description_" + id]
			del db["name_" + id]
			db["user_id_" + user_id] = users_ids
			return redirect(url + "dashboard", 302)
		except:
			return render_template('error.html', code = "401", user_name=request.headers['X-Replit-User-Name'], siteName=siteName, message = "Non sei il proprietario di questa nota.")

@app.route('/edt', methods=['POST'])
def editEntry():
	id = request.form["id"]
	global siteName
	global url
	if len(request.headers['X-Replit-User-Id']) != 0:
		desc = request.form['description']
		note = request.form['note']
		try:
			db["note_" + id] = note
			db["description_" + id] = desc
			return redirect(url + "dashboard", 302)
		except:
			return render_template('error.html', code = "401", siteName=siteName, message = "Non sei il proprietario di questa nota.", user_name=request.headers['X-Replit-User-Name'])

@app.route('/Fasm.ga.sxcu')
def sharexuploader():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'Fasm.ga_255.sxcu')

@app.route("/robots.txt")
def robots():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'robots.txt')

@app.route('/note/<key>', methods=['GET'])
def getNote(key):
    global siteName
    if request.headers["X-Replit-User-Id"]:
        try:
            notez = "note_" + key
            namez = "name_" + key
            descriptionz = "description_" + key
            return render_template("note.html", user_name=request.headers["X-Replit-User-Name"], siteName=siteName, note=db[notez], description=db[descriptionz], name=db[namez])
        except:
            return render_template('error.html', user_name=request.headers["X-Replit-User-Name"], code = "404", siteName=siteName, message = "Nota non esistente")
    else:
        try:
            notez = "note_" + key
            namez = "name_" + key
            descriptionz = "description_" + key
            return render_template("note_nologin.html", siteName=siteName, note=db[notez], description=db[descriptionz], name=db[namez])
        except:
            return render_template('error_nologin.html', code = "404", siteName=siteName, message = "Nota non esistente")

@app.route('/note/<key>/', methods=['GET'])
def getNote2(key):
    global siteName
    if request.headers["X-Replit-User-Id"]:
        try:
            notez = "note_" + key
            namez = "name_" + key
            descriptionz = "description_" + key
            return render_template("note.html", user_name=request.headers["X-Replit-User-Name"], siteName=siteName, note=db[notez], description=db[descriptionz], name=db[namez])
        except:
            return render_template('error.html', user_name=request.headers["X-Replit-User-Name"], code = "404", siteName=siteName, message = "Nota non esistente")
    else:
        try:
            notez = "note_" + key
            namez = "name_" + key
            descriptionz = "description_" + key
            return render_template("note_nologin.html", siteName=siteName, note=db[notez], description=db[descriptionz], name=db[namez])
        except:
            return render_template('error_nologin.html', code = "404", siteName=siteName, message = "Nota non esistente")

@app.route('/new', methods=['POST'])
def newEntry():
    global siteName
    if len(request.headers['X-Replit-User-Id']) != 0:
        if len(request.form["note"]) <= 255:
            if len(request.form["description"]) <= 50:
                if len(request.form["name"]) <= 30:
                    val = newString()
                    note = "note_" + val
                    desc = "description_" + val
                    name = "name_" + val
                    keys = list(db.keys())
                    while note in keys:
                        note = "note_" + val
                        keys = list(db.keys())
                    db[note] = request.form['note']
                    db[desc] = request.form['description']
                    db[name] = request.form['name']
                    try:
                        strings = list(getStrings(request.headers['X-Replit-User-Id']))
                    except:
                        strings = []
                    strings.append(note)
                    db["user_id_" + request.headers['X-Replit-User-Id']] = strings
                    return render_template('done.html', siteName=siteName, newNote = url + "note/" + val, user_name=request.headers['X-Replit-User-Name'])
                else:
                    return render_template("error.html", siteName = siteName, code = "TOO_LONG_NAME", message = "Il nome della nota supera i 30 caratteri.")
            else:
                return render_template("error.html", siteName = siteName, code = "TOO_LONG_DESCRIPTION", message = "La descrizione della nota supera i 50 caratteri.")
        else:
            return render_template("error.html", siteName = siteName, code = "TOO_LONG_NOTE", message = "La nota supera i 255 caratteri.")
    else:
        return redirect("/", 302)

@app.errorhandler(400)
def error_bad_request(e):
	global siteName
	if request.headers["X-Replit-User-Id"]:
		return render_template('error.html', siteName=siteName, code = "400", message = "Richiesta formulata in modo errato.", user_name=request.headers["X-Replit-User-Name"])
	else:
		return render_template('error_nologin.html', siteName=siteName, code = "400", message = "Richiesta formulata in modo errato.")

@app.errorhandler(401)
def error_unauthorized(e):
	global siteName
	if request.headers["X-Replit-User-Id"]:
		return render_template('error.html', siteName=siteName, code = "401", message = "Non autorizzato.", user_name=request.headers["X-Replit-User-Name"])
	else:
		return render_template('error_nologin.html', siteName=siteName, code = "401", message = "Non autorizzato.")

@app.errorhandler(403)
def error_forbidden(e):
	global siteName
	if request.headers["X-Replit-User-Id"]:
		return render_template('error.html', siteName=siteName, code = "403", message = "Accesso vietato.", user_name=request.headers["X-Replit-User-Name"] )
	else:
		return render_template('error_nologin.html', siteName=siteName, code = "403", message = "Accesso vietato.")

@app.errorhandler(404)
def error_page_not_found(e):
	global siteName
	if request.headers["X-Replit-User-Id"]:
		return render_template('error.html', siteName=siteName, code = "404", message = "Pagina non trovata.", user_name=request.headers["X-Replit-User-Name"] )
	else:
		return render_template('error_nologin.html', siteName=siteName, code = "404", message = "Pagina non trovata.")

@app.errorhandler(409)
def error_conflict(e):
	global siteName
	if request.headers["X-Replit-User-Id"]:
		return render_template('error.html', siteName=siteName, code = "409", message = "Conflitto.", user_name=request.headers["X-Replit-User-Name"] )
	else:
		return render_template('error_nologin.html', siteName=siteName, code = "409", message = "Conflitto.")

@app.errorhandler(501)
def error_internal_server_error(e):
	global siteName
	if request.headers["X-Replit-User-Id"]:
		return render_template('error.html', siteName=siteName, code = "501", message = "Errore interno del server.", user_name=request.headers["X-Replit-User-Name"] )
	else:
		return render_template('error_nologin.html', siteName=siteName, code = "501", message = "Errore interno del server.")

@app.errorhandler(502)
def error_bad_gateway(e):
	global siteName
	if request.headers["X-Replit-User-Id"]:
		return render_template('error.html', siteName=siteName, code = "502", message = "Gateway non funzionante.", user_name=request.headers["X-Replit-User-Name"] )
	else:
		return render_template('error_nologin.html', siteName=siteName, code = "502", message = "Gateway non funzionante.")

app.run(host='0.0.0.0', port=8080)