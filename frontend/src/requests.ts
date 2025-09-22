export type User = {name: string; username: string }
export type UserList = Array <User & {password: string}>

export async function login(username:String, password: string) {
    const request = await fetch ('/users.json')
    const usersJson: UserList = await request.json()
    return usersJson.find(s => s.password === password && s.username === username)
}

export async function getUser() {
    const request = await fetch ('/current.json')
    const user: User = await request.json()
    return user
}