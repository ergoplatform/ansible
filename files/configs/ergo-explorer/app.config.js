var __APP_CONFIG__ = {
  apiUrl: 'https://api-testnet.ergoplatform.com',
  alternativeLogo: false, // true by default
  environments: [
     {
       name: 'Testnet',
       url: 'https://testnet.ergoplatform.com',
     },
     {
       name: 'Mainnet',
       url: 'https://explorer.ergoplatform.com',
     },
   ],
};

if (typeof global !== 'undefined') {
  global.__APP_CONFIG__ = __APP_CONFIG__;
}
