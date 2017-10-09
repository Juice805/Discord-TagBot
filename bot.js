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

// Prevent Heroku Sleep

setInterval(function() {
	http.get("http://discord-tagbot.herokuapp.com");
}, 300000); // every 5 minutes (300000)

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

// ************************************* \\
// Bot On Ready
// ************************************* \\

client.on('ready', () => {
	console.log('Logged in as');
	console.log(client.user.username);
	console.log(client.user.id);
	console.log('Member of ' + client.guilds.array().length + ' servers.');
	console.log('---------');

	// Send a message to the owner
	const owner = client.fetchUser(process.env.COMMANDO_OWNER);
	owner.then(function(user) {
		user.send("I'm Awake!");
	}, function(error) {
		console.log('Unable to message owner: ' + error);
	})
});

// ************************************* \\
// Bot On Message
// ************************************* \\

client.on('guildCreate', guild => {

	// Change bot nickname on server join
	const member = guild.member(client.user);
	member.setNickname('Tag');

	// TODO: Add server to database
	console.log(`Joined Server: ${guild.name}`);

});

// ************************************* \\
// Bot On Message
// ************************************* \\

client.on('message', message => {

	// Ignore bots own messages
	if (message.author === client.user) {
		return;
	}

	if (message.content === 'hey') {
		message.reply('hello!');
	}
});




// Setup Complete, Login
client.login(process.env.DISCORD_TOKEN);