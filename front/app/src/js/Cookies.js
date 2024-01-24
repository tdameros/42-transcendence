export class Cookies {

    static get(name) {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let c = cookies[i].trim();
            if (c.indexOf(name) === 0) {
                return c.substring(name.length + 1, c.length);
            }
        }
        return null;
    }

    static add(name, value) {
        document.cookie = name + '=' + value + ';path=/;SameSite=Strict;Secure';
    }

    static remove(name) {
        document.cookie = name + '=;expires=Thu, 01 Jan 1970 00:00:01 GMT;path=/;SameSite=Strict;Secure';
    }
}

export default { Cookies };