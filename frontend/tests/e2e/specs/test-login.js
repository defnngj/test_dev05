// https://docs.cypress.io/api/introduction/api.html

describe('登录测试', () => {
  it('帐号为空', () => {
    cy.visit('/')
    cy.get('[cy-data=username]', { timeout: 3000}).clear()
    cy.get('[cy-data=password]', { timeout: 3000}).clear().type('admin123456')
    cy.get('[cy-data=loginBtn]', { timeout: 3000}).click()
    cy.contains('请输入账号')
  });
  it('密码为空', () => {
    cy.visit('/')
    cy.get('[cy-data=username]', { timeout: 3000}).clear().type('admin')
    cy.get('[cy-data=password]', { timeout: 3000}).clear()
    cy.get('[cy-data=loginBtn]', { timeout: 3000}).click()
    cy.contains('请输入密码')
  });
  it('用户名密码为空', () => {
    cy.visit('/')
    cy.get('[cy-data=username]', { timeout: 3000}).clear().type('error')
    cy.get('[cy-data=password]', { timeout: 3000}).clear().type('error123456')
    cy.get('[cy-data=loginBtn]', { timeout: 3000}).click()
    cy.contains('用户名密码错误')
  });
  it('登录成功', () => {
    cy.visit('/')
    cy.get('[cy-data=username]', { timeout: 3000}).clear().type('admin')
    cy.get('[cy-data=password]', { timeout: 3000}).clear().type('admin123456')
    cy.get('[cy-data=loginBtn]', { timeout: 3000}).click()
    // cy.contains('h1', 'Welcome to Your Vue.js App')
  })
})
