import jsonwebtoken from "jsonwebtoken";

export function generateAccessToken(username, userId) {
  return jsonwebtoken.sign({ username: username, userId: userId }, process.env.TOKEN_SECRET, { algorithm: 'HS256' });
}


export function tokenRequired(req, res, next) {
  let token = req.cookies.token
  if (token == null) return res.status(403).send({ 'message': 'a valid token is missing' })

  jsonwebtoken.verify(token, process.env.TOKEN_SECRET, (err, data) => {
    if (err) return res.sendStatus(403)
    req.user = data.user
    req.userId = data.userId
    next()
  })
}
