/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
      "./nonebot_plugin_pcr_sign/resources/templates/*.{html,js,jinja2}"
  ],
  theme: {
      extend: {
        fontFamily: {
          'Maoken': ['MaokenZhuyuanTi']
        },
      },
  },
}

