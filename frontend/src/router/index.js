import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue'),
    },
    {
      path: '/produtos',
      name: 'products',
      component: () => import('../views/ProductsView.vue'),
    },
    {
      path: '/produto/:id',
      name: 'product-detail',
      component: () => import('../views/ProductDetail.vue'),
    },
    {
      path: '/categorias',
      name: 'categories',
      component: () => import('../views/CategoriesView.vue'),
    },
    {
      path: '/contato',
      name: 'contact',
      component: () => import('../views/ContactView.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
    },
    {
      path: '/dashboard',
      meta: { requiresAuth: true },
      children: [
        {
          path: 'dono',
          name: 'dashboard-owner',
          component: () => import('../views/DashboardOwner.vue'),
          meta: { role: 'owner' },
        },
        {
          path: 'anunciador',
          name: 'dashboard-advertiser',
          component: () => import('../views/DashboardAdvertiser.vue'),
          meta: { role: 'advertiser' },
        },
        {
          path: 'produtos',
          name: 'dashboard-products',
          component: () => import('../views/DashboardProducts.vue'),
        },
        {
          path: 'produtos/novo',
          name: 'new-product',
          component: () => import('../views/NewProduct.vue'),
        },
        {
          path: 'produtos/:id/editar',
          name: 'edit-product',
          component: () => import('../views/EditProduct.vue'),
        },
      ],
    },
  ],
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    } else {
      return { top: 0 };
    }
  },
});

// Guard de autenticação
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('accessToken');
  const userRole = localStorage.getItem('userRole');

  if (to.meta.requiresAuth && !token) {
    next('/login');
  } else if (to.meta.role && to.meta.role !== userRole) {
    next('/');
  } else {
    next();
  }
});

export default router;
