describe('Admin - Editar Professores', () => {
  beforeEach(() => {
    cy.visit('/admin');
    cy.get('input[name="username"]').type('admin');
    cy.get('input[name="password"]').type('123');
    cy.get('input[type="submit"]').click();
    cy.visit('/admin');
  });

  it('deve editar professores', () => {
    const timestamp = Date.now();
    cy.visit('/admin/auth/user/2/change/');
    cy.contains('Modificar usuário').should('exist');
    cy.get('input[name="first_name"]').type(`nome${timestamp}`);    
    cy.get('input[name="last_name"]').type(`sobrenome${timestamp}`);    
    cy.get('input[type="submit"][value="Salvar"]').click();
    cy.contains('foi alterado com sucesso.').should('exist');
  });
});
