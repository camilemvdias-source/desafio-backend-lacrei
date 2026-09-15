# Deploy e Rollback

## Ambientes

- **Staging**: branch `develop` → deploy automático via GitHub Actions para um ambiente AWS Elastic Beanstalk (ou ECS) de staging.
- **Produção**: branch `main` → deploy automático (job `deploy` do workflow) após passar por lint, testes e build.

## Estratégia de deploy

Deploy via imagem Docker publicada em um registro (ECR) e implantada em Elastic Beanstalk/ECS. O job `build` do CI gera a imagem versionada com o SHA do commit, e o job `deploy` publica essa mesma versão.

## Rollback

Estratégia recomendada: **Blue/Green Deployment** (nativo no Elastic Beanstalk e no ECS):

1. Toda imagem publicada é taggeada com o SHA do commit (`lacrei-saude-api:<sha>`), nunca sobrescrevendo `latest` diretamente em produção.
2. Um novo deploy sobe um ambiente "green" ao lado do "blue" (o atual em produção).
3. Após smoke tests no ambiente green, o tráfego é apontado para ele.
4. Se algo der errado, basta reapontar o tráfego para o ambiente "blue" anterior (rollback em segundos, sem novo deploy).

Alternativa mais simples (sem infraestrutura Blue/Green): reverter o commit no GitHub e deixar o pipeline de CI/CD rodar o deploy automático da versão anterior (`git revert` + push), ou usar a opção "Redeploy" de uma versão anterior específica no Elastic Beanstalk.

## Migrações de banco

Migrações rodam automaticamente no start do container web (`python manage.py migrate`). Em caso de rollback que envolva uma migração destrutiva, uma migração reversa deve ser aplicada manualmente antes de reverter o código.
