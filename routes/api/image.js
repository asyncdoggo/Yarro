import { Router } from 'express';
import jsonwebtoken from 'jsonwebtoken';
import { tokenRequired } from '../../middlewares/jwt.js';
import User from '../../models/user.js';
var imageRouter = Router();

imageRouter.get('/:id', async function (req, res) {
    const id = req.params.id
    const path = `/public/userimages/${id}.png`
    if (fs.existsSync(path)) {
        return res.sendFile(path)
    }
    return res.sendFile("/public/userimages/default.png")
});


imageRouter.post("/", async function (req, res) {
    const file = req.file
})



export default imageRouter;
