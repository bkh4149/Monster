from flask import Flask, render_template, request, session, jsonify
from random import choice

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# モンスターのプリセット
monsters = [
    {"name": "Goblin", "hp": 50, "ap": 5, "dp": 2, "image": "a1.JPG"},
    {"name": "Troll", "hp": 80, "ap": 8, "dp": 5, "image": "a2.JPG"},
    {"name": "Dragon", "hp": 100, "ap": 10, "dp": 7, "image": "a3.JPG"},
    {"name": "Slime", "hp": 20, "ap": 3, "dp": 1, "image": "a4.JPG"},
    {"name": "Witch", "hp": 60, "ap": 7, "dp": 3, "image": "a5.JPG"}
]

def initialize_battle():
    """戦闘を初期化し、ランダムな敵を選択する"""
    enemy = choice(monsters)
    player = {"hp": 100, "ap": 10, "dp": 4}
    session['player'] = player
    session['enemy'] = enemy
    return enemy

def calculate_damage(attacker, defender):
    """ダメージ計算を行う"""
    damage = max(attacker['ap'] - defender['dp'], 0)
    return damage

@app.route('/')
def index():
    """初期ページの表示"""
    return render_template('index.html')

@app.route('/start', methods=['GET'])
def start_battle():
    """戦闘開始と敵の初期化"""
    enemy = initialize_battle()
    return jsonify({"message": "A wild {} appears!".format(enemy['name']), "enemy": enemy, "player": session['player']})

@app.route('/action', methods=['POST'])
def player_action():
    """プレイヤーのアクションを処理する"""
    action = request.json.get('action')
    player = session['player']
    enemy = session['enemy']
    print(f"app.py@46 {enemy=}  {player=}")
    #app.py@46 enemy={'ap': 3, 'dp': 1, 'hp': 20, 'image': 'a4.JPG', 'name': 'Slime'}  player={'ap': 10, 'dp': 4, 'hp': 100}
    if player['hp'] <= 0 or enemy['hp'] <= 0:
        return jsonify({"message": "Battle is already over.", "winner": "Player" if enemy['hp'] <= 0 else "Enemy"})
    
    result = ""
    
    if action == 1:  # 攻撃
        damage_to_enemy = calculate_damage(player, enemy)
        damage_to_player = calculate_damage(enemy, player)
        enemy['hp'] -= damage_to_enemy
        player['hp'] -= damage_to_player
        #result = "Player attacks for {} damage! Enemy attacks for {} damage!".format(damage_to_enemy, damage_to_player)
        session['enemy'] = enemy  # 更新された敵のデータをセッションに保存
        session['player'] = player  # 更新されたプレイヤーのデータをセッションに保存
        result = f"Player attacks for {damage_to_enemy} damage! Enemy attacks for {damage_to_player} damage!"
    # 他のアクションも同様にセッションを更新

    elif action == 2:  # 防御
        damage_to_player = calculate_damage(enemy, player) // 2
        player['hp'] -= damage_to_player
        result = "Player defends! Enemy attacks for {} damage!".format(damage_to_player)

    elif action == 3:  # 薬草
        player['hp'] += 20
        session['player'] = player  # 更新されたプレイヤーのデータをセッションに保存        
        result = "Player uses a herb and recovers 20 HP!"

    elif action == 4:  # 逃げる
        return jsonify({"message": "Player fled the battle.", "winner": "Enemy"})
    
    if player['hp'] <= 0 or enemy['hp'] <= 0:
        result += " Battle ended."
        winner = "Player" if enemy['hp'] <= 0 else "Enemy"
        return jsonify({"message": result, "winner": winner,  "enemy": enemy, "player": player})

    return jsonify({"message": result, "enemy": enemy, "player": player})

if __name__ == '__main__':
    app.run(debug=True)
