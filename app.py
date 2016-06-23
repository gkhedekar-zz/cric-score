from flask import Flask, render_template, redirect
from flask import request, jsonify, url_for
from datetime import datetime
import http_status
import datastore
app = Flask(__name__)
 
@app.route('/')
def get_message():
    return "Hello! This is the message from the server.. Yipee!"

@app.route('/team/<team_name>', methods=['GET'])
def get_team(team_name):
    try:
        content = datastore.Team.get_team(name=team_name)
        # return jsonify(content), http_status.SUCCESS
        return render_template('team.html', team=content)
    except Exception as e:
        return str(e)

@app.route('/create_team', methods=['POST'])
def create_team():
    try:
        team_name = request.form['team_name']
        datastore.Team.create_team(team_name)
        return redirect(url_for('home'))
    except Exception as e:
        return str(e)

@app.route('/home', methods=['GET', 'POST'])
def home():
    try:
        teams = datastore.Team.get_teams()
        matches = datastore.Match.get_matches()
        content = {
            'teams': teams,
            'matches': matches,
            'time': datetime.now().date(),
        }
        return render_template('home.html', data=content)
    except Exception as e:
        return str(e)

@app.route('/create_match', methods=['POST'])
def create_match():
    try:
        match_id = datastore.Match.create_match(request.form)
        return redirect(url_for('show_match', match_id=match_id))
    except Exception as e:
        return str(e)


@app.route('/match/<match_id>', methods=['GET', 'POST'])
def show_match(match_id):
    try:
        match = datastore.Match.get_match(id=match_id)
        return render_template('match.html', match=match)
    except Exception as e:
        return str(e)

@app.route('/update_player/<team_id>/<player_id>/<player_name>')
def update_player(team_id, player_id, player_name):
    return datastore.Player.update_player(player_name)
    return redirect(url_for('team', team_id=team_id))

@app.route('/update_players/<team_name>', methods=['POST'])
def update_players(team_name):
    players = []
    for (key, value) in request.form.iteritems():
        if 'player' in key:
            id = int(key.split('_')[1])
            player = datastore.Player.get_player(id=id)
            player.name = value
            players.append(player)
    datastore.Player.update_players(players)
    return redirect(url_for('get_team', team_name=team_name))

@app.route('/new_ball/<match_id>', methods=['POST'])
def new_ball(match_id):
    datastore.Ball.create_ball(match_id, request.form)
    return redirect(url_for('show_match', match_id=match_id))

if __name__ == "__main__":
    app.run(debug=True)