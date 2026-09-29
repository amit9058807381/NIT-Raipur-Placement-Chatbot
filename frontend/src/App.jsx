import { useEffect, useState } from "react";
import Login from "./Login";
import Register from "./Register";

function App() {
  // ==============================
  // USER
  // ==============================

  const [user, setUser] = useState(() => {
    const savedUser = localStorage.getItem("user");

    return savedUser ? JSON.parse(savedUser) : null;
  });

  const [showRegister, setShowRegister] = useState(false);

  // ==============================
  // CHAT STATES
  // ==============================

  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [conversationId, setConversationId] = useState("");
  const [chatHistory, setChatHistory] = useState([]);

  // Chat delete menu
  const [contextMenu, setContextMenu] = useState(null);

  // User right-click menu
  const [userMenu, setUserMenu] = useState(null);

  // ==============================
  // LOGIN
  // ==============================

  const handleLogin = (data) => {
    const loggedInUser = {
      name: data.name,
      email: data.email,
    };

    localStorage.setItem(
      "user",
      JSON.stringify(loggedInUser)
    );

    setUser(loggedInUser);
  };

  // ==============================
  // REGISTER
  // ==============================

  const handleRegister = (registeredUser) => {
    if (registeredUser) {
      setUser(registeredUser);
      setShowRegister(false);
    } else {
      setShowRegister(false);
    }
  };

  // ==============================
  // LOGOUT
  // ==============================

  const handleLogout = () => {
    localStorage.removeItem("user");

    setUser(null);

    setConversationId("");
    setMessages([]);
    setChatHistory([]);
    setMessage("");

    setContextMenu(null);
    setUserMenu(null);
  };

  // ==============================
  // LOAD CHAT HISTORY
  // ==============================

  const loadChatHistory = async () => {
    if (!user?.email) {
      return;
    }

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/api/conversations?email=${encodeURIComponent(
          user.email
        )}`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.error ||
            "Unable to load chat history"
        );
      }

      setChatHistory(data);

    } catch (error) {
      console.error(
        "History error:",
        error
      );
    }
  };

  // ==============================
  // LOAD HISTORY AFTER LOGIN
  // ==============================

  useEffect(() => {
    if (user?.email) {
      loadChatHistory();
    }
  }, [user]);

  // ==============================
  // CREATE NEW CHAT
  // ==============================

  const createNewChat = async () => {
    if (!user?.email) {
      return;
    }

    try {
      const response = await fetch(
        "http://127.0.0.1:5000/api/conversations",
        {
          method: "POST",
          headers: {
            "Content-Type":
              "application/json",
          },
          body: JSON.stringify({
            email: user.email,
          }),
        }
      );

      const data =
        await response.json();

      if (!response.ok) {
        throw new Error(
          data.error ||
            "Unable to create chat"
        );
      }

      setConversationId(
        data.conversation_id
      );

      setMessages([]);

      await loadChatHistory();

      setContextMenu(null);
      setUserMenu(null);

    } catch (error) {
      console.error(
        "New chat error:",
        error
      );
    }
  };

  // ==============================
  // OPEN EXISTING CHAT
  // ==============================

  const openChat = async (id) => {
    console.log(
      "Opening conversation:",
      id
    );

    if (!id) {
      console.error(
        "Conversation ID is missing"
      );
      return;
    }

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/api/conversations/${id}?email=${encodeURIComponent(
          user.email
        )}`
      );

      const data =
        await response.json();

      console.log(
        "Conversation response:",
        data
      );

      if (!response.ok) {
        throw new Error(
          data.error ||
            "Unable to load conversation"
        );
      }

      setConversationId(id);

      setMessages(
        Array.isArray(data)
          ? data
          : data.messages || []
      );

      setContextMenu(null);
      setUserMenu(null);

    } catch (error) {
      console.error(
        "Open chat error:",
        error
      );
    }
  };

  // ==============================
  // DELETE CHAT
  // ==============================

  const deleteChat = async (id) => {
    console.log(
      "Deleting conversation:",
      id
    );

    if (!id) {
      console.error(
        "Conversation ID is missing"
      );
      return;
    }

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/api/conversations/${id}?email=${encodeURIComponent(
          user.email
        )}`,
        {
          method: "DELETE",
        }
      );

      const data =
        await response.json();

      if (!response.ok) {
        throw new Error(
          data.error ||
            "Unable to delete chat"
        );
      }

      setChatHistory((prev) =>
        prev.filter(
          (chat) =>
            String(chat._id) !==
            String(id)
        )
      );

      if (
        String(conversationId) ===
        String(id)
      ) {
        setConversationId("");
        setMessages([]);
      }

      setContextMenu(null);

    } catch (error) {
      console.error(
        "Delete chat error:",
        error
      );
    }
  };

  // ==============================
  // SEND MESSAGE
  // ==============================

  const sendMessage = async () => {
    if (!message.trim()) {
      return;
    }

    if (!user?.email) {
      return;
    }

    const userMessage =
      message.trim();

    setMessage("");

    let currentConversationId =
      conversationId;

    try {
      // ==============================
      // AUTO CREATE CHAT
      // ==============================

      if (!currentConversationId) {
        const createResponse =
          await fetch(
            "http://127.0.0.1:5000/api/conversations",
            {
              method: "POST",
              headers: {
                "Content-Type":
                  "application/json",
              },
              body: JSON.stringify({
                email: user.email,
              }),
            }
          );

        const createData =
          await createResponse.json();

        if (!createResponse.ok) {
          throw new Error(
            createData.error ||
              "Unable to create chat"
          );
        }

        currentConversationId =
          createData.conversation_id;

        setConversationId(
          currentConversationId
        );

        setMessages([
          {
            role: "user",
            content: userMessage,
          },
        ]);

      } else {
        setMessages((prev) => [
          ...prev,
          {
            role: "user",
            content: userMessage,
          },
        ]);
      }

      // ==============================
      // SEND QUESTION
      // ==============================

      const response =
        await fetch(
          "http://127.0.0.1:5000/api/chat",
          {
            method: "POST",
            headers: {
              "Content-Type":
                "application/json",
            },
            body: JSON.stringify({
              email: user.email,
              conversation_id:
                currentConversationId,
              query: userMessage,
            }),
          }
        );

      const data =
        await response.json();

      if (!response.ok) {
        throw new Error(
          data.error ||
            "Something went wrong"
        );
      }

      // ==============================
      // AI RESPONSE
      // ==============================

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.answer,
        },
      ]);

      // ==============================
      // UPDATE SIDEBAR
      // ==============================

      await loadChatHistory();

    } catch (error) {
      console.error(
        "Send message error:",
        error
      );

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "Something went wrong. Please try again.",
        },
      ]);
    }
  };

  // ==============================
  // CLOSE MENUS
  // ==============================

  useEffect(() => {
    const closeMenu = () => {
      setContextMenu(null);
      setUserMenu(null);
    };

    document.addEventListener(
      "click",
      closeMenu
    );

    return () => {
      document.removeEventListener(
        "click",
        closeMenu
      );
    };
  }, []);

  // ==============================
  // LOGIN / REGISTER
  // ==============================

  if (!user) {
    if (showRegister) {
      return (
        <Register
          onRegister={
            handleRegister
          }
        />
      );
    }

    return (
      <Login
        onLogin={handleLogin}
        onRegister={() =>
          setShowRegister(true)
        }
      />
    );
  }

  // ==============================
  // MAIN CHAT PAGE
  // ==============================

  return (
    <div
      className="app"
      onClick={() => {
        setContextMenu(null);
        setUserMenu(null);
      }}
    >

      {/* =========================
          SIDEBAR
      ========================== */}

      <aside className="sidebar">

        <h2>
          NIT Placement AI
        </h2>

        <button
          className="new-chat"
          onClick={(e) => {
            e.stopPropagation();
            createNewChat();
          }}
        >
          + New Chat
        </button>

        {/* CHAT HISTORY */}

        <div className="history">

          <p>
            CHAT HISTORY
          </p>

          {chatHistory.length === 0 ? (

            <div className="chat-item">
              No chats yet
            </div>

          ) : (

            chatHistory.map(
              (chat) => {

                const chatId =
                  String(chat._id);

                return (
                  <div
                    key={chatId}
                    className={
                      "chat-item " +
                      (
                        conversationId ===
                        chatId
                          ? "active-chat"
                          : ""
                      )
                    }

                    onClick={(e) => {
                      e.stopPropagation();
                      openChat(chatId);
                    }}

                    onContextMenu={(e) => {

                      e.preventDefault();
                      e.stopPropagation();

                      setContextMenu({
                        id: chatId,
                        x: e.clientX,
                        y: e.clientY,
                      });

                      setUserMenu(null);
                    }}
                  >
                    {
                      chat.title ||
                      "New Chat"
                    }
                  </div>
                );
              }
            )

          )}

        </div>

        {/* =========================
            USER SECTION
        ========================== */}

            <div
  className="user-section"
  onContextMenu={(e) => {
    e.preventDefault();
    e.stopPropagation();

    setContextMenu(null);

    setUserMenu({
      x: e.clientX,
      y: e.clientY,
    });
  }}
>
  👤 {user.name}
</div>
      </aside>

      {/* =========================
          CHAT AREA
      ========================== */}

      <main className="chat-area">

        <div className="chat-header">
          NIT Raipur Placement Assistant
        </div>

        <div className="messages">

          {messages.length === 0 ? (

            <div className="welcome">

              <h1>
                How can I help you?
              </h1>

              <p>
                Ask about NIT Raipur
                placement and
                interview experiences.
              </p>

            </div>

          ) : (

            messages.map(
              (msg, index) => (

                <div
                  key={index}
                  className={
                    "message " +
                    msg.role
                  }
                >

                  <strong>
                    {
                      msg.role ===
                      "user"
                        ? "You"
                        : "AI"
                    }
                  </strong>

                  <p>
                    {msg.content}
                  </p>

                </div>

              )
            )

          )}

        </div>

        {/* INPUT */}

        <div className="input-area">

          <input
            type="text"
            placeholder="Ask a placement question..."
            value={message}
            onChange={(e) =>
              setMessage(
                e.target.value
              )
            }
            onKeyDown={(e) => {

              if (
                e.key === "Enter"
              ) {
                sendMessage();
              }

            }}
          />

          <button
            onClick={sendMessage}
          >
            Send
          </button>

        </div>

      </main>

      {/* =========================
          CHAT DELETE MENU
      ========================== */}

      {contextMenu && (

        <div
          className="context-menu"
          style={{
            position: "fixed",
            left: contextMenu.x,
            top: contextMenu.y,
          }}
          onClick={(e) => {
            e.stopPropagation();
          }}
        >

          <button
            onClick={() =>
              deleteChat(
                contextMenu.id
              )
            }
          >
            Delete chat
          </button>

        </div>

      )}

      {/* =========================
          USER MENU
      ========================== */}

      {userMenu && (

        <div
          className="context-menu user-menu"
          style={{
  position: "fixed",
  left: userMenu.x,
  top: userMenu.y - 100,
}}
          onClick={(e) => {
            e.stopPropagation();
          }}
        >

          <div className="user-email">
            {user.email}
          </div>

          <button
            onClick={() => {
              setUserMenu(null);
              handleLogout();
            }}
          >
            Logout
          </button>

        </div>

      )}

    </div>
  );
}

export default App;