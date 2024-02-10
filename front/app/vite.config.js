import {defineConfig} from 'vite';
import path from 'path';

export default defineConfig({
  server: {
    port: 8080,
  },
  resolve: {
    alias: {
      '@utils': path.resolve(__dirname, 'src/js/utils/'),
      '@components': path.resolve(__dirname, 'src/js/components/'),
      '@pages': path.resolve(__dirname, 'src/js/components/pages/'),
      '@css': path.resolve(__dirname, 'src/css/'),
      '@img': path.resolve(__dirname, 'src/img/'),
      '@fonts': path.resolve(__dirname, 'src/fonts/'),
      '@js': path.resolve(__dirname, 'src/js/'),
    },
  },
});
