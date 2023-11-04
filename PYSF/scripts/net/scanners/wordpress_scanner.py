from lib import print_utils
from lib import var_util

INFO = {
    "name": "Wordpress Scanner",
    "variables": ["URL"],
    "variables_description": ["The URL to scan. This should be the base URL of the site"],
    "Variables_type": ["string"],
    "variables_default": [""],
    "variables_required": [True],
    "description": "Scans a wordpress site for pages that wordpress commonly uses",
    "requirements": []
}

def main(variables):
    try:
        import requests
    except:
        print_utils.error("requests is not installed. Please install it with 'pip3 install requests'")
        return 1
    url = var_util.get_var_data(variables, "URL")
    paths = ["/index.php", "/license.txt", "/readme.html", "/wp-activate.php", "/wp-app.php", "/wp-blog-header.php", "/wp-comments-post.php", "/wp-config-sample.php", "/wp-cron.php", "/wp-links-opml.php", "/wp-load.php", "/wp-login.php", "/wp-mail.php", "/wp-pass.php", "/wp-register.php", "/wp-settings.php", "/wp-signup.php", "/wp-trackback.php", "/xmlrpc.php", "/wp-admin/about.php", "/wp-admin/admin-ajax.php", "/wp-admin/admin-footer.php", "/wp-admin/admin-functions.php", "/wp-admin/admin-header.php", "/wp-admin/admin-post.php", "/wp-admin/admin.php", "/wp-admin/async-upload.php", "/wp-admin/comment.php", "/wp-admin/credits.php", "/wp-admin/custom-background.php", "/wp-admin/custom-header.php", "/wp-admin/edit-comments.php", "/wp-admin/edit-form-advanced.php", "/wp-admin/edit-form-comment.php", "/wp-admin/edit-link-form.php", "/wp-admin/edit-tag-form.php", "/wp-admin/edit-tags.php", "/wp-admin/edit.php", "/wp-admin/export.php", "/wp-admin/freedoms.php", "/wp-admin/gears-manifest.php", "/wp-admin/import.php", "/wp-admin/index-extra.php", "/wp-admin/index.php", "/wp-admin/install-helper.php", "/wp-admin/install.php", "/wp-admin/link-add.php", "/wp-admin/link-manager.php", "/wp-admin/link-parse-opml.php", "/wp-admin/link.php", "/wp-admin/load-scripts.php", "/wp-admin/load-styles.php", "/wp-admin/media-new.php", "/wp-admin/media-upload.php", "/wp-admin/media.php", "/wp-admin/menu-header.php", "/wp-admin/menu.php", "/wp-admin/moderation.php", "/wp-admin/ms-admin.php", "/wp-admin/ms-delete-site.php", "/wp-admin/ms-edit.php", "/wp-admin/ms-options.php", "/wp-admin/ms-sites.php", "/wp-admin/ms-themes.php", "/wp-admin/ms-upgrade-network.php", "/wp-admin/ms-users.php", "/wp-admin/my-sites.php", "/wp-admin/nav-menus.php", "/wp-admin/network/admin.php", "/wp-admin/network/edit.php", "/wp-admin/network/index-extra.php", "/wp-admin/network/index.php", "/wp-admin/network/menu.php", "/wp-admin/network/plugin-editor.php"]
    for path in paths:
        response = requests.get(url + path)
        if response.status_code == 200:
            print_utils.success(f"Found {url + path}")
        elif response.status_code == 403 or response.status_code == 401:
            print_utils.warn(f"Found {url + path} but got a {response.status_code} response")
        else:
            print_utils.error(f"Request to {url + path} returned {response.status_code}")