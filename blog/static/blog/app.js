console.log('Web interface loaded');

const usernameInput = document.querySelector('.username-input')
const passwordInput = document.querySelector('.password-input')
const loginBtn = document.querySelector('.login-button')
const loginMsg = document.querySelector('.login-message')

loginBtn.addEventListener('click', async () => {
    const usernameValue = usernameInput.value
    const passwordValue = passwordInput.value
    
    const response = await fetch('/api/token/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: usernameValue,
            password: passwordValue,
        }),
    })

    const data = await response.json()
    console.log(data)

    if (response.ok) {
        localStorage.setItem('accessToken', data.access)
        loginMsg.textContent = 'Вход выполнен'
    } else {
        loginMsg.textContent = 'Неверное имя пользователя или пароль'
    }

});

const tagNameInput = document.querySelector('.tag-name')
const createTagBtn = document.querySelector('.create-tag-button')
const tagMsg = document.querySelector('.tag-message')

createTagBtn.addEventListener('click', async () => {
    const tagName = tagNameInput.value
    const accessToken = localStorage.getItem('accessToken')

    if (!accessToken) {
        tagMsg.textContent = 'Сначала выполните вход'
        return
    }

    const response = await fetch('/api/tags/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${accessToken}`
        },
        body: JSON.stringify({
            name: tagName,
        })
    })

    const createdTag = await response.json()

    if (response.ok) {
        tagMsg.textContent = `Тег "${createdTag.name}" создан`
        tagNameInput.value = ''
        loadTags()
    } else {
        tagMsg.textContent = JSON.stringify(createdTag)
    }
})

async function loadTags() {
    const response = await fetch('/api/tags/')
    const tags = await response.json()

    postTags.innerHTML = ''

    tags.forEach(tagData => {
        const option = document.createElement('option')

        option.value = tagData.id
        option.textContent = tagData.name

        postTags.appendChild(option)
    })
}

const loadPosts = document.querySelector('.load-posts-button')
const postsContainer = document.querySelector('.posts-container')

const changePostContainer = document.querySelector('.change-post-container')
const changePostTitle = document.querySelector('.change-post-title')
const changePostContent = document.querySelector('.change-post-content')
const saveChangesBtn = document.querySelector('.save-changes-button')
const stopChangesBtn = document.querySelector('.stop-changes-button')
const changesMsg = document.querySelector('.changes-message')

loadPosts.addEventListener('click', async () => {
    const response = await fetch('/api/posts/')

    const posts = await response.json()

    postsContainer.innerHTML = ''

    posts.forEach(postData => {
        const postElement = document.createElement('div')
        postElement.classList.add('post-content')

        const titleElement = document.createElement('h3')
        titleElement.textContent = postData.title

        const contentElement = document.createElement('p')
        contentElement.textContent = postData.content

        const contentAuthor = document.createElement('p')
        contentAuthor.textContent = `Автор: ${postData.author}`

        const contentTags = document.createElement('p')
        contentTags.textContent = postData.tag_names
            .map(tagName => `#${tagName}`)
            .join(' ')

        const deletePost = document.createElement('button')
        deletePost.textContent = 'Удалить'
        deletePost.classList.add('delete-post-button')

        const changePost = document.createElement('button')
        changePost.textContent = 'Изменить'
        changePost.classList.add('change-post-button')

        const commentPostBtn = document.createElement('button')
        commentPostBtn.textContent = 'Комментировать'

        postElement.appendChild(titleElement)
        postElement.appendChild(contentElement)
        postElement.appendChild(contentAuthor)
        postElement.appendChild(contentTags)
        postElement.appendChild(deletePost)
        postElement.appendChild(changePost)
        postElement.appendChild(commentPostBtn)

        postsContainer.appendChild(postElement)

        deletePost.addEventListener('click', async () => {
            const accessToken = localStorage.getItem('accessToken')
            if (!accessToken) {
                postMsg.textContent = 'Сначала выполните вход'
                return 
            }

            const response = await fetch(`/api/posts/${postData.id}/`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${accessToken}`,
                }
            })

            if (response.ok) {
                postElement.remove()
            } else {
                postMsg.textContent = 'Не удалось удалить пост'
            }

        })

        changePost.addEventListener('click', async () => {
            changePostContainer.hidden = false
            
            changePostTitle.value = postData.title
            changePostContent.value = postData.content

            changePostContainer.dataset.postId = postData.id
        })

        commentPostBtn.addEventListener('click', () => {
            commentPostID.value = postData.id
            commentContent.focus()
        })
    });
    
    saveChangesBtn.addEventListener('click', async () => {
        const postId = changePostContainer.dataset.postId
        const newTitle = changePostTitle.value
        const newContent = changePostContent.value

        const accessToken = localStorage.getItem('accessToken')
        if (!accessToken) {
            changesMsg.textContent = 'Сначала выполните вход'
            return
        }

        const response = await fetch(`/api/posts/${postId}/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`,
            },
            body: JSON.stringify({
                title: newTitle,
                content: newContent,
            }),
        })

        const updatedPost = await response.json()

        if (response.ok) {
            postMsg.textContent = 'Пост обновлен'
            changePostContainer.hidden = true
            loadPosts.click()
        } else {
            postMsg.textContent = JSON.stringify(updatedPost)
        }
    })

    stopChangesBtn.addEventListener('click', () => {
        changePostContainer.hidden = true
        changesMsg.textContent = ''
    })

})

const postTitle = document.querySelector('.post-title')
const postTextArea = document.querySelector('.create-post-content')
const postTags = document.querySelector('.post-tags')
const postBtn = document.querySelector('.create-post-button')
const postMsg = document.querySelector('.post-message')


postBtn.addEventListener('click', async () => {
    const titleValue = postTitle.value
    const textareaValue = postTextArea.value
    const tagsValue = postTags.value
    
    const accessToken = localStorage.getItem('accessToken')

    const tagIds = Array.from(postTags.selectedOptions)
    .map(option => Number(option.value))

    if (!accessToken) {
        postMsg.textContent = 'Сначала выполните вход'
        return
    }

    const response = await fetch('/api/posts/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${accessToken}`,
        },
        body: JSON.stringify({
            title: titleValue,
            content: textareaValue,
            tags: tagIds,
        }),
    })

    const data = await response.json()

    if (response.ok) {
        postMsg.textContent = 'Пост создан'
        postTitle.value = ''
        postTextArea.value = ''
        postTags.value = ''

        loadPosts.click()
    } else {
        postMsg.textContent = JSON.stringify(data)
        
    }
})

const loadCommentsBtn = document.querySelector('.load-comments-button')
const commentsContainer = document.querySelector('.comments-container')
const commentPostID = document.querySelector('.comment-post-id')
const commentContent = document.querySelector('.comment-content')
const createCommentBtn = document.querySelector('.create-comment-button')
const commentMsg = document.querySelector('.comment-message')

loadCommentsBtn.addEventListener('click', async () => {
    const response = await fetch('/api/comments/')
    const comments = await response.json()

    commentsContainer.textContent = ''

    comments.forEach(commentData => {
        const commentElement = document.createElement('div')
        commentElement.classList.add('comment')

        const commentText = document.createElement('p')
        commentText.textContent = commentData.content

        const commentAuthor = document.createElement('p')
        commentAuthor.textContent = `Автор: ${commentData.author}`

        const commentPost = document.createElement('p')
        commentPost.textContent = `ID поста: ${commentData.post}`

        const deleteCommentBtn = document.createElement('button')
        deleteCommentBtn.textContent = 'Удалить'
        deleteCommentBtn.classList.add('delete-comment-button')

        commentElement.appendChild(commentText)
        commentElement.appendChild(commentAuthor)
        commentElement.appendChild(commentPost)
        commentElement.appendChild(deleteCommentBtn)

        commentsContainer.appendChild(commentElement)

        deleteCommentBtn.addEventListener('click', async () => {
            const accessToken = localStorage.getItem('accessToken')

            if (!accessToken) {
                commentMsg.textContent = 'Сначала выполните вход'
                return
            }

            const response = await fetch(
                `/api/comments/${commentData.id}/`,
                {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${accessToken}`,
                    },
                }
            )

            if (response.ok) {
                commentElement.remove()
                commentMsg.textContent = 'Комментарий удалён'
            } else {
                commentMsg.textContent = 'Не удалось удалить комментарий'
            }
        })
    })   
})

createCommentBtn.addEventListener('click', async () => {
    const postId = commentPostID.value
    const contentValue = commentContent.value
    const accessToken = localStorage.getItem('accessToken')

    if (!accessToken) {
        commentMsg.textContent = 'Сначала выполните вход'
        return
    }

    const response = await fetch('/api/comments/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${accessToken}`,
        },
        body: JSON.stringify({
            post: Number(postId),
            content: contentValue
        }),
    })

    const createdComment = await response.json()

    if (response.ok) {
        commentContent.value = ''
    } else {
        commentMsg.textContent = JSON.parse(createdComment)
    }
})


const socket = new WebSocket(
    `ws://${window.location.host}/ws/comments/`
)
/*
new WebSocket(...) — создаёт постоянное соединение с сервером;
ws:// — протокол WebSocket, аналог http://;
window.location.host — текущий адрес сайта, сейчас это 127.0.0.1:8000;
/ws/comments/ — маршрут, который мы создали в routing.py.
*/

socket.onopen = () => {
    console.log('WebSocket подключен')
}

socket.onmessage = (event) => {
    const newComment = JSON.parse(event.data)

    console.log('Получен новый комментарий:', newComment)

    commentMsg.textContent =
        `Новый комментарий от ${newComment.author}`

    loadCommentsBtn.click()
}

loadPosts.click()
loadCommentsBtn.click()
loadTags()

