from flask import Flask, request, jsonify
from flask_restful import Api, Resource

# Data contoh olahraga yang lebih lengkap
sports = [
    {"id": "1", "name": "Berenang", "description": "Olahraga yang baik untuk kekuatan otot dan kesehatan jantung.", "calories_burned": 500},
    {"id": "2", "name": "Lari", "description": "Membantu meningkatkan stamina dan membakar kalori dengan cepat.", "calories_burned": 600},
    {"id": "3", "name": "Bersepeda", "description": "Olahraga kardiovaskular yang rendah dampak dan menyenangkan.", "calories_burned": 400},
    {"id": "4", "name": "Yoga", "description": "Meningkatkan fleksibilitas dan relaksasi mental.", "calories_burned": 200},
    {"id": "5", "name": "Basketball", "description": "Olahraga tim yang meningkatkan kecepatan dan koordinasi.", "calories_burned": 700},
    {"id": "6", "name": "Bola Voli", "description": "Meningkatkan kekuatan otot dan kerja tim.", "calories_burned": 300},
    {"id": "7", "name": "Gimnastik", "description": "Olahraga yang melibatkan gerakan tubuh yang terampil dan beragam.", "calories_burned": 350},
    {"id": "8", "name": "Pilates", "description": "Meningkatkan kekuatan inti dan fleksibilitas tubuh.", "calories_burned": 250},
    {"id": "9", "name": "Rugby", "description": "Olahraga kontak yang membutuhkan kekuatan dan strategi.", "calories_burned": 800},
    {"id": "10", "name": "Senam Aerobik", "description": "Latihan yang menyenangkan untuk kebugaran jantung.", "calories_burned": 400}
]

# Detail olahraga yang lebih lengkap
sport_details = {sport['id']: sport for sport in sports}

app = Flask(__name__)
api = Api(app)

class SportList(Resource):
    def get(self):
        return {
            "error": False,
            "message": "success",
            "count": len(sports),
            "sports": sports
        }

class SportDetail(Resource):
    def get(self, sport_id):
        if sport_id in sport_details:
            return {
                "error": False,
                "message": "success",
                "sport": sport_details[sport_id]
            }
        return {"error": True, "message": "Sport not found"}, 404

class AddSport(Resource):
    def post(self):
        data = request.get_json()
        new_sport = {
            "id": str(len(sports) + 1),  # Generate a new ID
            "name": data.get('name'),
            "description": data.get('description'),
            "calories_burned": data.get('calories_burned')
        }
        sports.append(new_sport)
        sport_details[new_sport['id']] = new_sport
        return {
            "error": False,
            "message": "Sport added successfully",
            "sport": new_sport
        }, 201

class UpdateSport(Resource):
    def put(self, sport_id):
        data = request.get_json()
        if sport_id in sport_details:
            sport_to_update = sport_details[sport_id]
            sport_to_update['name'] = data.get('name', sport_to_update['name'])
            sport_to_update['description'] = data.get('description', sport_to_update['description'])
            sport_to_update['calories_burned'] = data.get('calories_burned', sport_to_update['calories_burned'])
            return {
                "error": False,
                "message": "Sport updated successfully",
                "sport": sport_to_update
            }
        return {"error": True, "message": "Sport not found"}, 404

class DeleteSport(Resource):
    def delete(self, sport_id):
        if sport_id in sport_details:
            sports.remove(sport_details[sport_id])
            del sport_details[sport_id]
            return {
                "error": False,
                "message": "Sport deleted successfully"
            }
        return {"error": True, "message": "Sport not found"}, 404

# Menambahkan resource ke API
api.add_resource(SportList, '/sports')
api.add_resource(SportDetail, '/sports/<string:sport_id>')
api.add_resource(AddSport, '/sports/add')
api.add_resource(UpdateSport, '/sports/update/<string:sport_id>')
api.add_resource(DeleteSport, '/sports/delete/<string:sport_id>')

if __name__ == '__main__':
    app.run(debug=True)
