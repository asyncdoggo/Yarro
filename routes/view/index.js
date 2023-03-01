import { Router } from 'express';
var indexRouter = Router();

indexRouter.get('/', function(req, res, next) {
  res.render('index.html');
});

export default indexRouter;
