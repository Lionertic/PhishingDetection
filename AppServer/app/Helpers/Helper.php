<?php

function isUrl($url) {
      $regex = "((https?|ftp)\:\/\/)?([a-z0-9+!*(),;?&=\$_.-]+(\:[a-z0-9+!*(),;?&=\$_.-]+)?@)?([a-z0-9-.]*)\.([a-z]{2,3})(\:[0-9]{2,5})?(\/([a-z0-9+\$_-]\.?)+)*\/?(\?[a-z+&\$_.-][a-z0-9;:@&%=+\/\$_.-]*)?(#[a-z_.-][a-z0-9+\$_.-]*)?";

      if(preg_match("/^$regex$/", $url)) { 
            return true; 
      } else {
            $regex = "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}";
            if(preg_match("/^$regex$/", $url)) { 
                  return true; 
            } else {
                  return false;
            }
      }
}
function addScheme($url, $scheme = 'http://'){
      return parse_url($url, PHP_URL_SCHEME) === null ? $scheme . $url : $url;
}