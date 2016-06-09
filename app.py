from flask import Flask, render_template
from flask import request, jsonify, url_for
import http_status
import datastore
app = Flask(__name__)
 
@app.route('/')
def get_message():
    return "Hello! This is the message from the server.. Yipee!"

@app.route('/team/<team_id>')
def get_team(team_id):
    try:
        content = datastore.Team.get_team(id=team_id)
        return jsonify(content), http_status.SUCCESS
    except:
        return "Getting team failed"

@app.route('/create_team/<team_name>')
def create_team(team_name):
    try:
        datastore.Team.create_team(team_name)
        return "Success"
    except:
        return "Failed"

@app.route('/create_match')
def create_match():
    try:
        datastore.match.create_match(team1, team2)
        return "Success"
    except:
        return "Failed"

@app.route('/update_player/<team_id>/<player_id>/<player_name>')
def update_player(team_id, player_id, player_name):
    return datastore.Player.update_player(player_name)
    return redirect(url_for('team', team_id=team_id))


if __name__ == "__main__":
    app.run(debug=True)