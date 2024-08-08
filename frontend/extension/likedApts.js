import { getLikedApts } from './fetchLikedApts.js'

export function likedApts() {

    const userData = {
        user_name: sessionStorage.getItem('user_name')
      };
    const liked_apts = getLikedApts(userData)
    console.log("Liked apts:", liked_apts)
    }