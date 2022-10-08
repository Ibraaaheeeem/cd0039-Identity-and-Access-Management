/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'mycoffeeshop2022.us', // the auth0 domain prefix
    audience: 'https://120.0.0.1:8080/buy', // the audience set for the auth0 app
    clientId: 'FSWEaV30Ec7ifcsctoU3xk1nMMrEeLMZ', // the client id generated for the auth0 app
    callbackURL: 'http://127.0.0.1:8080', // the base url of the running ionic application. 
  }
};
