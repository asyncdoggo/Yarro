import mongoose from "mongoose";


const userSchema = new mongoose.Schema({
    _id: {
        type: mongoose.Schema.ObjectId,
    },
    username: {
        type: String,
        required: true,
        unique: true
    },
    password: {
        type: String,
        required: true
    },
    email: {
        type: String,
        required: true,
        unique: true
    },
    confirmed: {
        type: Boolean,
        required: true
    },
    name: {
        type: String,
    },
    age: {
        type: Number,
    },
    gender: {
        type: String,
        enum: ["Male", "Female", "Other"]
    },
    dob: {
        type: Date,
    },
    bio: {
        type: String,
    },
    created_at: {
        type: Date,
        default: Date.now
    },
    posts: [{
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Post'
    }],
    likes: [{
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Post'
    }],
    dislikes: [{
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Post'
    }]
})



export default mongoose.model("User", userSchema)