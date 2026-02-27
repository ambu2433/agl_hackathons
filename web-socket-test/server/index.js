import express from "express";
import {webSocketServer} from "ws";

const app = express();
const port = 8080;

const server = app.listen(port, () => {

    console.log("server is listening ... ");
})

const wss= new WsbSocketServer({ server}) ;

wss.on("connection", (ws) => {
 console.log("data fdrom client :", data);
 ws.send("thanks buddy");
 //ws.send("message", (data) = {})

})

