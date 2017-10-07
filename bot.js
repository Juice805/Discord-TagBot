//const Discord = require('discord.js');
const commando = require('discord.js-commando');
const path = require('path');
const http = require('http');
const fs = require('fs');
const sqlite = require('sqlite');

// ************************************* \\
// Simple response to HTTP requests
// ************************************* \\

http.createServer(function(req, res) {
	data = "Bot is running!";
	res.writeHead(200, {
		'Content-Type': 'text/html',
		'Content-Length': data.length
	});
	res.write(data);
	res.end();
}).listen(process.env.PORT);

// ************************************* \\
// Commando
// ************************************* \\

// For standard Discord JS API use
//const client = new Discord.Client();

// For Commando Use
const client = new commando.Client({
	owner: process.env.COMMANDO_OWNER,
	commandPrefix: '<'
});

// ************************************* \\
// Commando Group Registration
// ************************************* \\

client.registry
	// Registers your custom command groups
	.registerGroups([
		['admin', 'Admin Only'],
		['everyone', 'Everyone'],
		['misc', 'Miscellaneous'],
		['util', 'Utility']
	])

// Registers all built-in groups, commands, and argument types
//.registerDefaults()

.registerDefaultTypes()

.registerDefaultCommands({
	help: true,
	eval_: false,
	prefix: false,
	ping: false,
	commandState: false
})

// Registers all of your commands in the ./commands/ directory
.registerCommandsIn(path.join(__dirname, 'commands'));

client.on('ready', () => {
	console.log('I am ready!');
	const owner = client.fetchUser(process.env.COMMANDO_OWNER);
	owner.then(function(user) {
		user.send('Hello World!');
	}, function(error) {
		console.log('Unable to message owner: ' + error);
	})
});

client.on('message', message => {
	if (message.content === 'ping') {
		message.reply('pong');
	}
});

client.login(process.env.DISCORD_TOKEN);