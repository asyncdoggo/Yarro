
import mongoose from "mongoose";

const PostSchema = new mongoose.Schema({
  _id: {
    type: mongoose.Schema.ObjectId
  },
  author: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User'
  },
  content: {
    type: String,
    required: true
  },
  content_type: {
    type: String,
    required: true
  },
  created_at: {
    type: Date,
    default: Date.now
  },
  likes: [{
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User'
  }],
  dislikes: [{
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User'
  }]
});


export default mongoose.model("Post", PostSchema)