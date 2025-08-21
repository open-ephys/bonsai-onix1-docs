import WorkflowContainer from "./workflow.js"

export default {
  iconLinks: [
    {
      icon: 'github',
      href: 'https://github.com/open-ephys/onix1-bonsai-docs',
      title: 'GitHub'
    },
    {
      icon: 'twitter-x',
      href: 'https://x.com/openephys',
      title: 'X (Twitter)'
    },
    {
      icon: 'discord',
      href: 'https://discord.gg/WXAx2URNQU',
      title: 'Discord'
    }
  ],
  start: () => {
      WorkflowContainer.init();
  }
}
