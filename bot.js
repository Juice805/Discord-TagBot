const Discord = require('discord.js');
const client = new Discord.Client();

const http = require('http');
const fs = require('fs');

http.createServer(function(req, res) {
	data = "Bot is running!";
	res.writeHead(200, {
		'Content-Type': 'text/html',
		'Content-Length': data.length
	});
	res.write(data);
	res.end();
}).listen(process.env.PORT);

client.on('ready', () => {
	console.log('I am ready!');
});

client.on('message', message => {
	if (message.content === 'ping') {
		message.reply('pong');
	}
});

client.login(process.env.DISCORD_TOKEN);