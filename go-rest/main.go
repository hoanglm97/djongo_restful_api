package main

// import required library
import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/gorilla/mux"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

var collection *mongo.Collection

// Person represents a person document in MongoDB
type UserAccount struct {
	ID          primitive.ObjectID `json:"_id,omitempty" bson:"_id,omitempty"`
	Name        string             `json:"name,omitempty" bson:"name,omitempty"`
	Age         int                `json:"age,omitempty" bson:"age,omitempty"`
	Description string             `json:"description,omitempty" bson:"description,omitempty"`
}

// create User:
// if methods == Post => set content-type == application/json
// let user == UserAccount, decode request.Body
// grant _id == user.Id == id.primitive.ObjectId
// encode user and push data in Mongo
func createUser(response http.ResponseWriter, request *http.Request) {
	if request.Method == "POST" {
		response.Header().Set("content-type", "application/json")
		var user UserAccount
		json.NewDecoder(request.Body).Decode(&user)
		ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
		defer cancel()
		result, _ := collection.InsertOne(ctx, user)
		id := result.InsertedID
		user.ID = id.(primitive.ObjectID)
		json.NewEncoder(response).Encode(user)
	} else {
		http.Error(response, "Invalid method.", 405)
	}

}

// get one user by Id
func getUserByID(response http.ResponseWriter, request *http.Request) {
	if request.Method == "GET" {
		response.Header().Set("content-type", "application/json")
		var user UserAccount
		id, _ := primitive.ObjectIDFromHex(mux.Vars(request)["id"])
		ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
		defer cancel()
		err := collection.FindOne(ctx, UserAccount{ID: id}).Decode(&user)
		if err != nil {
			response.WriteHeader(http.StatusInternalServerError)
			response.Write([]byte(`{ "message": "` + err.Error() + `" }`))
			return
		}
		json.NewEncoder(response).Encode(user)
	}

}

func getAllUser(response http.ResponseWriter, request *http.Request) {
	if request.Method == "GET" {
		response.Header().Set("content-type", "application/json")
		var people []UserAccount
		ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
		defer cancel()
		cursor, err := collection.Find(ctx, bson.M{})
		if err != nil {
			response.WriteHeader(http.StatusInternalServerError)
			response.Write([]byte(`{ "message": "` + err.Error() + `" }`))
			return
		}
		defer cursor.Close(ctx)
		for cursor.Next(ctx) {
			var person UserAccount
			cursor.Decode(&person)
			people = append(people, person)
		}
		if err := cursor.Err(); err != nil {
			response.WriteHeader(http.StatusInternalServerError)
			response.Write([]byte(`{ "message": "` + err.Error() + `" }`))
			return
		}
		json.NewEncoder(response).Encode(people)
	}
}

func updateUser(response http.ResponseWriter, request *http.Request) {
	if request.Method == "PUT" {
		response.Header().Set("content-type", "application/json")
		var user UserAccount
		id, _ := primitive.ObjectIDFromHex(mux.Vars(request)["id"])
		json.NewDecoder(request.Body).Decode(&user)
		ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
		defer cancel()
		result, err := collection.UpdateOne(ctx, UserAccount{ID: id}, bson.M{"$set": user})
		if err != nil {
			response.WriteHeader(http.StatusInternalServerError)
			response.Write([]byte(`{ "message": "` + err.Error() + `" }`))
			return
		}
		json.NewEncoder(response).Encode(result)
	}
}

func deleteUser(response http.ResponseWriter, request *http.Request) {
	if request.Method == "DELETE" {
		response.Header().Set("content-type", "application/json")
		id, _ := primitive.ObjectIDFromHex(mux.Vars(request)["id"])
		ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
		defer cancel()
		result, err := collection.DeleteOne(ctx, UserAccount{ID: id})
		if err != nil {
			response.WriteHeader(http.StatusInternalServerError)
			response.Write([]byte(`{ "message": "` + err.Error() + `" }`))
			return
		}
		json.NewEncoder(response).Encode(result)
	}
}

func homePage(response http.ResponseWriter, request *http.Request) {
	fmt.Fprintf(response, "Welcome!")
}

func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	clientOptions := options.Client().ApplyURI("mongodb://localhost:27017")
	client, _ := mongo.Connect(ctx, clientOptions)
	collection = client.Database("example").Collection("people")
	router := mux.NewRouter().StrictSlash(true)
	router.HandleFunc("/", homePage)
	router.HandleFunc("/get", getAllUser).Methods("GET")
	router.HandleFunc("/get_user/{id}", getUserByID).Methods("GET")
	router.HandleFunc("/create", createUser).Methods("POST")
	router.HandleFunc("/edit_user/{id}", updateUser).Methods("PUT")
	router.HandleFunc("/delete_user/{id}", deleteUser).Methods("DELETE")
	log.Fatal(http.ListenAndServe(":8080", router))
}
