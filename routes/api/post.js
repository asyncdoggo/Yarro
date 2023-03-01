import { Router } from 'express';
import Post from '../../models/post.js';
import { tokenRequired } from '../../middlewares/jwt.js';
import mongoose from 'mongoose';
import User from '../../models/user.js';

var postRouter = Router();

// update like/dislike
postRouter.put('/', function (req, res) {
});


// create new post
postRouter.post('/', tokenRequired, async function (req, res) {
  try {
    const post = new Post({
      _id: new mongoose.Types.ObjectId(),
      author: req.body.author,
      content: req.body.content,
      content_type: req.body.content_type,
      likes: 0,
      dislikes: 0
    })
    await post.save();

    await User.updateOne(
      { _id: req.body.author },
      { $push: { posts: post._id } }
    );

    res.status(201).json({ message: "success" })

  }
  catch (err) {
    res.status(201).json({ message: err.message })
  }
})


// get posts
postRouter.get('/', tokenRequired, async function (req, res) {
  const posts = await Post.aggregate([
    {
      $lookup: {
        from: 'users',
        localField: 'author',
        foreignField: '_id',
        as: 'author'
      }
    },
    {
      $unwind: '$author'
    },
    {
      $lookup: {
        from: 'users',
        localField: 'likes',
        foreignField: '_id',
        as: 'likes'
      }
    },
    {
      $lookup: {
        from: 'users',
        localField: 'dislikes',
        foreignField: '_id',
        as: 'dislikes'
      }
    },
    {
      $addFields: {
        liked: {
          $in: [mongoose.Types.ObjectId(req.userId), '$likes._id']
        },
        disliked: {
          $in: [mongoose.Types.ObjectId(req.userId), '$dislikes._id']
        },
        likeCount: {
          $size: '$likes'
        },
        dislikeCount: {
          $size: '$dislikes'
        }
      }
    },
    {
      $project: {
        author: {
          _id: 1,
          username: 1
        },
        content: 1,
        created_at: 1,
        liked: 1,
        disliked: 1,
        likeCount: 1,
        dislikeCount: 1
      }
    }
  ])
})


// Delete posts
postRouter.delete('/', function (req, res) {

})





export default postRouter;
