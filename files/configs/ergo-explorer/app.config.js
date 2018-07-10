var __APP_CONFIG__ = {
  apiUrl: 'https://api-testnet.ergoplatform.com',
  environments: [
//     {
//       name: 'Mainnet',
//       url: 'https://ergoplatform.com',
//     },
     {
       name: 'Testnet',
       url: 'https://testnet.ergoplatform.com',
     },
   ],
};

if (typeof global !== 'undefined') {
  global.__APP_CONFIG__ = __APP_CONFIG__;
}
