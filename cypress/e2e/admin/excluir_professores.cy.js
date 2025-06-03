describe('Admin - Excluir Professores com segurança', () => {
  beforeEach(() => {
    cy.visit('/admin/login/');
    cy.get('input[name="username"]').type('admin');
    cy.get('input[name="password"]').type('123');
    cy.get('input[type="submit"]').click();
  });

  it('deve excluir um usuário que não seja o superuser', () => {
    cy.visit('/admin/auth/user/');

    cy.get('tr').each($row => {
      const $link = $row.find('th a');
      const username = $link.text().trim();
      const href = $link.attr('href');

      if (username && username !== 'admin' && href && href.includes('/change/')) {
        cy.visit(href);
        cy.get('a.deletelink').click(); 
        cy.contains('Remover').should('exist');
        cy.get('input[type="submit"]').click(); 
        cy.contains('foi removido com sucesso').should('exist');
        return false;
      }
    });
  });
});
