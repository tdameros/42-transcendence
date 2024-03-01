import {Component} from '@components';

export class PrivacyPolicyContent extends Component {
  constructor() {
    super();
  }
  render() {
    return (`
      <div class="m-2 card">
          <div class="card-header">
              <h2>Privacy policy</h2>
          </div>
          <div class="card-body">
              <p>
                  This Privacy Policy describes how Transcendence collects, uses, and shares users' personal information on our website. Cookies are small text files stored on your device that help websites, for example, personalize content and ads, provide social media features, and analyze traffic.
              </p>
              
              <p>
                  <strong>Collection and Use of Information</strong>
                  <br>
                  There are 4 main types of cookies:
                  <ul>
                      <li>Functionality cookies: These cookies are essential for the proper functioning of our website and allow us to offer you basic features, such as navigating pages and accessing secure areas.</li>
                      <li>Analytics cookies: These cookies collect information about how visitors use a website. These cookies help understand which pages are most popular, how visitors navigate the site, and how to improve the user experience.</li>
                      <li>Preference cookies: These cookies allow us to remember your browsing preferences and personalize the content of our site based on your interests.</li>
                      <li>Commercial purpose cookies: These cookies are used by companies for marketing, targeted advertising, and tracking user behavior.</li>
                  </ul>
                  We do not use or store any analytics cookies or cookies for commercial purposes. We only use functionality and preference cookies.
              </p>
              
              <p>
                  <strong>Sharing of Information</strong>
                  <br>
                  We do not sell, rent, or share your personal information with third parties for commercial purposes. However, we may disclose your information in the following cases:
                  <ul>
                      <li>When required by law or court order;</li>
                      <li>To protect our rights, safety, or property, as well as those of our users or other concerned parties;</li>
                  </ul>
              </p>
              
              <p>
                  <strong>Information Security</strong>
                  <br>
                  We implement technical, administrative, and physical security measures to protect your personal information against unauthorized access, misuse, or unauthorized disclosure.
              </p>
              
              <p>
                  <strong>Your Rights</strong>
                  <br>
                  You have the right to access, rectify, update, or delete your personal information. You can also object to the processing of your personal information or request the limitation of its use. To exercise these rights, you can update your personal information from your profile page, or choose to anonymize your personal data by deleting your account.
              </p>
              
              <p>
                  <strong>Changes to the Privacy Policy</strong>
                  <br>
                  We reserve the right to modify this Privacy Policy at any time. Any changes will be posted on this page with an updated revision date.
                  <br>
                  Last updated: 26/02/2024
              </p>
          </div>
      </div>
    `);
  }
  style() {
    return (`
      <style>

      </style>
    `);
  }
}
