// https://docs.cypress.io/api/introduction/api.html

describe('项目测试', () => {
  it('创建项目', () => {
    cy.visit('/')
    cy.get('[cy-data=username]', { timeout: 3000}).clear().type('admin')
    cy.get('[cy-data=password]', { timeout: 3000}).clear().type('admin123456')
    cy.get('[cy-data=loginBtn]', { timeout: 3000}).click()
    cy.visit('/#/main/project')
    cy.get('[cy-data=create-project]', { timeout: 3000}).click()
    cy.contains('创建项目')
    cy.get('[cy-data=project-name]', { timeout: 3000}).type('test-project')
    cy.get('[cy-data=project-desc]', { timeout: 3000}).type('desc')
    cy.get('[cy-data=project-status]', { timeout: 3000}).click()
    cy.get('[cy-data=project-status]', { timeout: 3000}).click()
    cy.get('[cy-data=save-project]', { timeout: 3000}).click()
    cy.contains('创建成功')
  });
  it('编辑项目', () => {
    cy.visit('/')
    cy.get('[cy-data=username]', { timeout: 3000}).clear().type('admin')
    cy.get('[cy-data=password]', { timeout: 3000}).clear().type('admin123456')
    cy.get('[cy-data=loginBtn]', { timeout: 3000}).click()
    cy.visit('/#/main/project')
    cy.get('[cy-data=edit-project]', { timeout: 3000}).first().click({ force: true })
    cy.contains('编辑项目')
    cy.get('[cy-data=project-name]', { timeout: 3000}).clear().type('edit-project')
    cy.get('[cy-data=project-desc]', { timeout: 3000}).clear().type('edit-desc')
    cy.get('[cy-data=project-status]', { timeout: 3000}).click()
    cy.get('[cy-data=project-status]', { timeout: 3000}).click()
    cy.get('[cy-data=save-project]', { timeout: 3000}).click()
    cy.contains('更新成功')
  });
  it('删除项目', () => {
    cy.visit('/')
    cy.get('[cy-data=username]', { timeout: 3000}).clear().type('admin')
    cy.get('[cy-data=password]', { timeout: 3000}).clear().type('admin123456')
    cy.get('[cy-data=loginBtn]', { timeout: 3000}).click()
    cy.visit('/#/main/project')
    cy.wait(2000)
    cy.get('[cy-data=delete-project]', { timeout: 3000}).first().click({ force: true })
    cy.contains('删除成功')
  });
  it('列表翻页', () => {
    cy.visit('/')
    cy.get('[cy-data=username]', { timeout: 3000}).clear().type('admin')
    cy.get('[cy-data=password]', { timeout: 3000}).clear().type('admin123456')
    cy.get('[cy-data=loginBtn]', { timeout: 3000}).click()
    cy.visit('/#/main/project')
    cy.wait(2000)
    cy.get('ul.el-pager > li.number', { timeout: 3000 }).eq(1).click() // 点击第2页
    cy.get('button.btn-next', { timeout: 3000 }).click() // 点击下一页
  });
})
