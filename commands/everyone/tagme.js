const commando = require('discord.js-commando');

module.exports = class TagMeCommand extends commando.Command {
	constructor(client) {
		super(client, {
			name: 'tagme',
			aliases: ['🏷me'],
			group: 'everyone',
			memberName: 'tagme',
			description: 'Tag yourself',
			examples: ['tagme awesome', 'tagme overwatch'],
			guildOnly: true,

			args: [{
				key: 'tags',
				label: 'tags',
				prompt: 'What would you like to tag yourself with?',
				type: 'string',
				infinite: true
			}]
		});
	}

	async run(msg, args) {
		const tags = args.tags;

		return msg.reply(`You have been tagged with ${tags}`);

		// 		const user = member.user;
		// 		return msg.reply(stripIndents `
		// 	Info on **${user.username}#${user.discriminator}** (ID: ${user.id})
		// 	**❯ Member Details**
		// 	${member.nickname !== null ? ` • Nickname: ${member.nickname}` : ' • No nickname'}
		// 	 • Roles: ${member.roles.map(roles => `\`${roles.name}\``).join(', ')}
		// 	 • Joined at: ${member.joinedAt}
		// 	**❯ User Details**
		// 	 • Created at: ${user.createdAt}${user.bot ? '\n • Is a bot account' : ''}
		// 	 • Status: ${user.presence.status}
		// 	 • Game: ${user.presence.game ? user.presence.game.name : 'None'}
		// `);
	}
};