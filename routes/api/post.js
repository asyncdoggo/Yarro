import { Router } from 'express';
import Post from '../../models/post.js';
import { tokenRequired } from '../../middlewares/jwt.js';
import mongoose from 'mongoose';
import User from '../../models/user.js';

var postRouter = Router();

// update like/dislike
postRouter.put('/', tokenRequired, async function (req, res) {


  const post = await Post.findById(req.body.postId);
  if (!post) {
    throw new Error('Post not found');
  }

  const user = await User.findById(req.userId);
  if (!user) {
    throw new Error('User not found');
  }

  let updateObj = {};
  if (req.body.isLike) {
    if (post.likes.includes(req.userId)) {
      updateObj = { $pull: { likes: req.userId } };
    } else {
      updateObj = {
        $addToSet: { likes: req.userId },
        $pull: { dislikes: req.userId },
      };
    }
  } else {
    if (post.dislikes.includes(req.userId)) {
      updateObj = { $pull: { dislikes: req.userId } };
    } else {
      updateObj = {
        $addToSet: { dislikes: req.userId },
        $pull: { likes: req.userId },
      };
    }
  }

  await Post.updateOne({ _id: req.body.postId }, updateObj);
  await User.updateOne(
    { _id: req.userId },
    {
      $addToSet: { [req.body.isLike ? 'likes' : 'dislikes']: req.body.postId },
      $pull: { [req.body.isLike ? 'dislikes' : 'likes']: req.body.postId },
    }
  );

  return res.json({ message: "success" });
});


// create new post
postRouter.post('/', async function (req, res) {
  try {
    const post = new Post({
      _id: new mongoose.Types.ObjectId(),
      author: req.body.author,
      content: req.body.content,
      content_type: req.body.content_type,
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
postRouter.get('/'/*, tokenRequired */, async function (req, res) {
  req.userId = "6400a7f490edf45186fa9fe5"
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
          $in: [new mongoose.Types.ObjectId(req.userId), '$likes._id']
        },
        disliked: {
          $in: [new mongoose.Types.ObjectId(req.userId), '$dislikes._id']
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



  return res.status(201).json({ message: "success", data: posts })

})


// Delete posts
postRouter.delete('/', function (req, res) {

})

export default postRouter;
